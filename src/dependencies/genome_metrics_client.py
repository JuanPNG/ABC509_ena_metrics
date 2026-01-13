import requests

from pydantic import ValidationError
from typing import Any, Dict
from .genome_metrics_schema import EnaAssemblyResponse, AssemblyMetrics
from .genome_metrics_normalise import extract_assembly_metrics

ENA_ASSEMBLY_URL = "https://www.ebi.ac.uk/ena/browser/api/summary"


def fetch_ena_assembly(accession: str, *, timeout_s: int = 30) -> Dict[str, Any]:
    """
    Fetch an ENA assembly record using the ENA summary endpoint.

    This function assumes the ENA summary API always returns a response of the form:
        {
          "summaries": [ { ...assembly record... } ],
          "total": "1"
        }

    Args:
        accession: ENA assembly accession (e.g. 'GCA_964035705').
        timeout_s: HTTP timeout in seconds.

    Returns:
        A dictionary representing the ENA assembly record
        (the first element of the 'summaries' array).

    Raises:
        ValueError: If no summaries are returned.
        TypeError: If the response shape is unexpected.
        requests.HTTPError: If the HTTP request fails.

    """
    url = f"{ENA_ASSEMBLY_URL}/{accession}"
    resp = requests.get(url, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()

    if not isinstance(payload, dict) or "summaries" not in payload:
        raise TypeError(f"Unexpected ENA summary response shape: {type(payload)}")

    summaries = payload.get("summaries") or []
    if not summaries:
        raise ValueError(f"No summaries returned for accession {accession}")

    # Enforce that the summary matches the requested accession
    record = summaries[0]
    if isinstance(record, dict) and record.get("accession") not in (None, accession):
        raise ValueError(
            f"ENA returned accession {record.get('accession')} for requested {accession}"
        )

    return record


def get_raw(accession: str) -> EnaAssemblyResponse:
    """
    Fetch + validate raw ENA record.
    """
    raw_payload = fetch_ena_assembly(accession)
    raw = EnaAssemblyResponse.model_validate(raw_payload)
    return raw


def get_assembly_metrics(accession: str) -> AssemblyMetrics:
    """
    Fetch + validate raw + extract normalised metrics (AssemblyMetrics).

    Example usage:
    ```python
    from dependencies.genome_metrics_client import get_assembly_metrics
    accession = "GCA_964035705"
    ex = get_assembly_metrics(accession)
    print(ex.model_dump()) # Complete assembly metrics record
    print(ex.scaffold_n50) # Access just one field
    ```
    """
    raw = get_raw(accession)
    return extract_assembly_metrics(raw)


def build_bq_record(accession: str) -> Dict[str, object]:
    """
    Build the ENA assembly summary metrics fragment suitable to be merged into a biodiversity data ingestion pipeline record.

    Output shape:
    {
      "accession": "...",
      "assembly_metrics": { ... } | None
    }

    Behavior:
        - On success, returns normalised assembly metrics.
        - On failure, returns a soft error payload without raising.

    Args:
        accession: ENA assembly accession.

    Returns:
        Dictionary containing the accession and assembly metrics fragment.

    Example usage:
    ```python
    from dependencies.genome_metrics_client import build_bq_record

    record = {
    "sample_id": "SAMPLE_001",
    "species": "Porites rus",
    "assembly_accession": "GCA_964035705",
    "pipeline_version": "2.4.1",
    }

    accession = record["assembly_accession"]

    ena_genome_metrics = build_bq_record(accession)

    print(ena_genome_metrics) # Complete assembly metrics record
    ```
    """
    try:
        raw_payload = fetch_ena_assembly(accession)
        raw = EnaAssemblyResponse.model_validate(raw_payload)

        assembly_metrics = extract_assembly_metrics(raw)

        return {
            "accession": raw.accession,
            "assembly_metrics": assembly_metrics.model_dump(),
        }

    except (ValidationError, ValueError, TypeError) as e:
        # Fail soft: pipeline decides what to do
        return {
            "accession": accession,
            "assembly_metrics": None,
            "assembly_metrics_error": f"{type(e).__name__}: {e}",
        }
