from typing import Any, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EnaAttribute(BaseModel):
    """
        Represents a single ENA assembly attribute as returned by the ENA Browser API.

        ENA encodes most assembly statistics as a list of tag/value pairs, where both
        elements are strings. These are later normalised into typed fields.

        Example (from ENA payload):
            {
                "tag": "scaffold-count",
                "value": "3096"
            }
    """
    model_config = ConfigDict(extra="forbid")
    tag: str
    value: str


class EnaChromosome(BaseModel):
    """
        Represents a chromosome or replicon entry in the ENA assembly record.

        Each entry describes a top-level sequence (chromosome, mitochondrion, plasmid)
        associated with the assembly.

        Fields:
            accession: List of INSDC accessions associated with this replicon.
            name: Human-readable name (e.g. '1', 'MT').
            type: Replicon type (e.g. 'Chromosome', 'Mitochondrion').
            count: Number of sequences represented (usually 1).
    """
    model_config = ConfigDict(extra="forbid")
    accession: List[str]
    name: str
    type: str
    count: int = Field(ge=0)


class EnaLink(BaseModel):
    """
        Represents a downloadable resource associated with an ENA assembly.

        Examples include:
            - WGS flatfile
            - FASTA sequence archive
    """
    model_config = ConfigDict(extra="forbid")
    label: str
    url: str


class EnaAssemblyResponse(BaseModel):
    """
    Validated representation of a raw ENA genome assembly summary record.

    This model corresponds to a *single* assembly record after client-side
    normalisation of ENA response shapes (direct record, list-wrapped, or
    search/summaries response).

    Responsibilities:
        - Enforce ENA schema expectations
        - Reject unexpected fields (extra='forbid')
        - Normalize selected fields (e.g. assemblyLevel)

    This model is intended for **internal use only**. Downstream pipelines
    should consume `AssemblyMetrics` instead.
    """
    model_config = ConfigDict(extra="forbid")

    accession: str
    title: str
    description: Optional[str] = None
    name: str
    version: int
    dataType: Literal["ASSEMBLY"]
    status: int
    statusDescription: str

    chromosomes: List[EnaChromosome] = Field(default_factory=list)

    wgsSet: Optional[str] = None
    assemblyType: Optional[str] = None
    assemblyLevel: Optional[str] = None
    platform: Optional[str] = None
    program: Optional[str] = None
    assemblyCoverage: Optional[float] = None

    attributes: List[EnaAttribute] = Field(default_factory=list)
    links: List[EnaLink] = Field(default_factory=list)

    @field_validator("assemblyLevel", mode="before")
    @classmethod
    def normalise_assembly_level(cls, v: Any) -> Any:
        """
        Normalise the assembly level string provided by ENA.

        ENA may vary casing or include surrounding whitespace. This validator
        ensures a canonical lowercase representation (e.g. 'chromosome').

        The validator runs in 'before' mode so normalization occurs prior
        to type coercion.
        """
        return v.strip().lower() if isinstance(v, str) else v


class AssemblyMetrics(BaseModel):
    """
    Normalized assembly quality metrics derived from an ENA assembly record.

    This model is the **primary downstream contract** exposed by this package.
    All fields are:
        - optional (to tolerate partial ENA records),
        - typed,
        - safe for direct serialisation to BigQuery.

    Metric tiers:
        Tier 1: Core usability indicators
        Tier 2: Assembly quality refinement
        Tier 3: Detailed contiguity diagnostics

    All values originate either from ENA top-level fields or from the
    attributes tag/value list after normalisation.
    """
    model_config = ConfigDict(extra="forbid")

    # Tier 1
    assembly_level: Optional[str] = None
    ungapped_length: Optional[int] = Field(default=None, ge=0)
    scaffold_n50: Optional[int] = Field(default=None, ge=0)
    scaffold_count: Optional[int] = Field(default=None, ge=0)

    # Tier 2
    contig_n50: Optional[int] = Field(default=None, ge=0)
    contig_count: Optional[int] = Field(default=None, ge=0)
    coverage: Optional[float] = Field(default=None, gt=0)
    spanned_gaps: Optional[int] = Field(default=None, ge=0)
    unspanned_gaps: Optional[int] = Field(default=None, ge=0)

    # Tier 3
    contig_l50: Optional[int] = Field(default=None, ge=0)
    scaffold_l50: Optional[int] = Field(default=None, ge=0)
    contig_n75: Optional[int] = Field(default=None, ge=0)
    contig_n90: Optional[int] = Field(default=None, ge=0)
    scaffold_n75: Optional[int] = Field(default=None, ge=0)
    scaffold_n90: Optional[int] = Field(default=None, ge=0)
    replicon_count: Optional[int] = Field(default=None, ge=0)
    non_chromosome_replicon_count: Optional[int] = Field(default=None, ge=0)


