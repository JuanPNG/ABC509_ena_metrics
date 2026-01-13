# ENA Genome Assembly metrics 

`dependencies` include a small, focused module for fetching, validating, and normalising
**ENA genome assembly quality metrics** from the ENA Browser API.

It is designed to be embedded into existing data ingestion pipelines and to produce
**BigQuery-safe assembly metrics** with minimal coupling.

To be added to metadata collection steps and as part of airflow dag dependencies. 

---

## What this package does

Given an ENA assembly accession (e.g. `GCA_964035705`), the package:

1. Fetches the corresponding ENA assembly record
2. Validates the payload using Pydantic
3. Normalizes ENA’s tag/value attributes into typed metrics
4. Returns a small, safe dictionary fragment for pipeline integration

---

## Installation

```bash
pip install -e .
```


## Quick start

```python
from dependencies.genome_metrics_client import build_bq_record

record = build_bq_record("GCA_964035705")

print(record)
```

Exxample output:

```python 
{
  "accession": "GCA_964035705",
  "assembly_metrics": {
    "assembly_level": "chromosome",
    "ungapped_length": 569490461,
    "scaffold_n50": 35060836,
    "scaffold_count": 3096,
    "contig_n50": 1779000,
    "contig_count": 3774,
    "coverage": 151.0,
    "spanned_gaps": 678,
    "unspanned_gaps": 0,
    "contig_l50": 99,
    "scaffold_l50": 6,
    "contig_n75": 761526,
    "contig_n90": 50202,
    "scaffold_n75": 28716807,
    "scaffold_n90": 120869,
    "replicon_count": 15,
    "non_chromosome_replicon_count": 1,
    "ena_last_updated": "2024-05-08"
  }
}
```
On failure:

```python
{
  "accession": "GCA_XXXXXXX",
  "assembly_metrics": None,
  "assembly_metrics_error": "ValidationError: ..."
}
```

## Intended pipeline usage

```python
from dependencies.genome_metrics_client import build_bq_record

pipeline_record = {
    "sample_id": "SAMPLE_001",
    "accession": "GCA_964035705",
}

ena_fragment = build_bq_record(pipeline_record["assembly_accession"])

pipeline_record["assembly_metrics"] = ena_fragment.get("assembly_metrics")
pipeline_record["assembly_metrics_error"] = ena_fragment.get("assembly_metrics_error")

```

## Assembly metrics schema

Assembly quality metrics are grouped into **tiers** to reflect their relative importance
and typical usage in downstream analyses.

### Tier 1 — Core usability

**Tier 1** metrics capture core assembly usability. These are the minimum indicators
  needed to decide whether an assembly is broadly suitable for most analyses.

* assembly_level 
* ungapped_length 
* scaffold_n50 
* scaffold_count

### Tier 2 — Quality refinement

**Tier 2** metrics provide additional resolution on assembly quality and contiguity.
  They are commonly used for comparative evaluation, filtering, and quality control
  beyond a simple pass/fail assessment.

* contig_n50 
* contig_count 
* coverage 
* spanned_gaps 
* unspanned_gaps

### Tier 3 — Detailed contiguity

**Tier 3** metrics offer fine-grained diagnostics intended for detailed inspection
  and troubleshooting. They are useful for understanding assembly structure but are
  not required for most routine analyses.

* contig_l50 
* scaffold_l50 
* contig_n75 
* contig_n90 
* scaffold_n75 
* scaffold_n90 
* replicon_count 
* non_chromosome_replicon_count

### Supporting

* ena_last_updated (string, as provided by ENA)

## Package structure

```bash
dependencies/
├── genome_metrics_client.py      # ENA API access + public API
├── genome_metrics_schema.py      # Pydantic models
├── genome_metrics_normalise.py   # Tag mapping and normalization logic
└── __init__.py
```

## Requirement

* Python ≥ 3.10 
* pydantic==2.12.5 
* requests>=2.31.0