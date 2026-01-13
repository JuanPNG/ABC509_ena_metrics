"""
dependencies

Utilities for fetching, validating, and normalizing ENA assembly
quality metrics for downstream data pipelines.
"""

from .genome_metrics_client import build_bq_record, fetch_ena_assembly
from .genome_metrics_schema import EnaAssemblyResponse, AssemblyMetrics

__all__ = [
    "build_bq_record",
    "fetch_ena_assembly",
    "EnaAssemblyResponse",
    "AssemblyMetrics",
]
