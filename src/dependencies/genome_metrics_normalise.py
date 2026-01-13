from typing import Dict
from .genome_metrics_schema import EnaAssemblyResponse, AssemblyMetrics


ENA_TAG_TO_KEY: Dict[str, str] = {
    "ungapped-length": "ungapped_length",
    "n50": "scaffold_n50",
    "scaffold-count": "scaffold_count",
    "count-contig": "contig_count",
    "contig-n50": "contig_n50",
    "contig-L50": "contig_l50",
    "contig-n75": "contig_n75",
    "contig-n90": "contig_n90",
    "scaf-L50": "scaffold_l50",
    "scaf-n75": "scaffold_n75",
    "scaf-n90": "scaffold_n90",
    "spanned-gaps": "spanned_gaps",
    "unspanned-gaps": "unspanned_gaps",
    "replicon-count": "replicon_count",
    "count-non-chromosome-replicon": "non_chromosome_replicon_count",
}

_INT_KEYS = {
    "ungapped_length",
    "scaffold_n50",
    "scaffold_count",
    "contig_n50",
    "contig_count",
    "spanned_gaps",
    "unspanned_gaps",
    "contig_l50",
    "scaffold_l50",
    "contig_n75",
    "contig_n90",
    "scaffold_n75",
    "scaffold_n90",
    "replicon_count",
    "non_chromosome_replicon_count",
}


def _coerce_value(key: str, raw_value: str):
    """
    Coerce ENA attribute values into explicit Python types.

    Numeric assembly metrics are converted to integers.
    All other values are returned as strings.
    """
    if key in _INT_KEYS:
        return int(raw_value)
    return raw_value


def extract_assembly_metrics(raw: EnaAssemblyResponse) -> AssemblyMetrics:
    """
    Extract and normalise assembly metrics from a validated ENA record.

    This function performs the transformation:
        EnaAssemblyResponse → AssemblyMetrics

    Steps:
        1. Pull selected metrics from ENA top-level fields
        2. Map ENA attribute tags to internal metric keys
        3. Coerce values into appropriate Python types
        4. Validate the result using AssemblyMetrics

    Args:
        raw: A validated ENA assembly record.

    Returns:
        AssemblyMetrics instance containing normalised metrics.

    Raises:
        ValidationError: If normalised data violates AssemblyMetrics constraints.
    """
    metric_data: Dict[str, object] = {}

    # Top-level fields
    if raw.assemblyLevel is not None:
        metric_data["assembly_level"] = raw.assemblyLevel
    if raw.assemblyCoverage is not None:
        metric_data["coverage"] = float(raw.assemblyCoverage)

    # Tag/value attributes
    for attr in raw.attributes:
        key = ENA_TAG_TO_KEY.get(attr.tag)
        if key is None:
            continue
        metric_data[key] = _coerce_value(key, attr.value)

    return AssemblyMetrics.model_validate(metric_data)
