"""Domain types for job posting analysis.

CUPID: Domain-based - types model the problem domain explicitly.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


class RequirementLevel(Enum):
    """Classification of job requirements."""

    MUST_HAVE = auto()
    NICE_TO_HAVE = auto()
    UNKNOWN = auto()


class ContractType(Enum):
    """Standard contract types."""

    CDI = "CDI"
    CDD = "CDD"
    FREELANCE = "Freelance"
    STAGE = "Stage"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str) -> "ContractType":
        """Parse contract type from string."""
        normalized = value.strip().upper()

        # Direct matches
        if normalized in ("CDI", "FULL-TIME", "TEMPS PLEIN"):
            return cls.CDI
        if normalized == "CDD":
            return cls.CDD
        if normalized == "FREELANCE":
            return cls.FREELANCE
        if normalized in ("STAGE", "INTERNSHIP"):
            return cls.STAGE

        return cls.UNKNOWN


@dataclass(frozen=True)
class Requirement:
    """A single job requirement with its classification.

    CUPID: Idiomatic - uses frozen dataclass for immutability.
    """

    text: str
    level: RequirementLevel = RequirementLevel.UNKNOWN

    @property
    def is_required(self) -> bool:
        """Check if this is a must-have requirement."""
        return self.level == RequirementLevel.MUST_HAVE

    @property
    def is_optional(self) -> bool:
        """Check if this is a nice-to-have requirement."""
        return self.level == RequirementLevel.NICE_TO_HAVE


@dataclass(frozen=True)
class Location:
    """Job location information.

    CUPID: Domain-based - models location as a value object.
    """

    city: str
    country: str = "France"
    remote_ok: bool = False

    def __str__(self) -> str:
        """Format location as string."""
        parts = [self.city]
        if self.country:
            parts.append(self.country)
        if self.remote_ok:
            parts.append("(Remote OK)")
        return ", ".join(parts)


@dataclass(frozen=True)
class Salary:
    """Salary information.

    CUPID: Domain-based - models salary as a value object.
    """

    raw: str
    min_value: int | None = None
    max_value: int | None = None
    currency: str = "EUR"

    def __str__(self) -> str:
        """Format salary as string."""
        return self.raw


@dataclass
class JobPosting:
    """Structured representation of a job posting.

    CUPID: Domain-based - the aggregate root of job posting domain.

    Uses explicit sentinel values instead of None where appropriate:
    - contract_type: ContractType.UNKNOWN instead of None
    - location/salary: Optional (None means "not specified")
    """

    title: str
    company: str
    location: Location | None = None
    contract_type: ContractType = ContractType.UNKNOWN
    salary: Salary | None = None
    must_have: list[str] = field(default_factory=list)
    nice_to_have: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    raw_text: str = ""

    @property
    def all_requirements(self) -> list[Requirement]:
        """Get all requirements with their levels."""
        requirements = []
        for text in self.must_have:
            requirements.append(Requirement(text, RequirementLevel.MUST_HAVE))
        for text in self.nice_to_have:
            requirements.append(Requirement(text, RequirementLevel.NICE_TO_HAVE))
        return requirements

    @property
    def keyword_count(self) -> int:
        """Count of ATS keywords."""
        return len(self.keywords)

    def has_keyword(self, keyword: str) -> bool:
        """Check if a keyword is present (case-insensitive)."""
        keyword_lower = keyword.lower()
        return any(k.lower() == keyword_lower for k in self.keywords)
