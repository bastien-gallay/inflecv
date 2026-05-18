"""Domain types for job fit analysis.

CUPID: Domain-based - types model the fit analysis domain explicitly.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


class FitLevel(Enum):
    """Classification of requirement match level."""

    SATISFIED = auto()      # ✅ Fully satisfied
    PARTIAL = auto()        # ⚠️ Partially satisfied
    NOT_SATISFIED = auto()  # ❌ Not satisfied

    @property
    def emoji(self) -> str:
        """Get emoji representation."""
        return {
            FitLevel.SATISFIED: "✅",
            FitLevel.PARTIAL: "⚠️",
            FitLevel.NOT_SATISFIED: "❌",
        }[self]

    @property
    def score(self) -> float:
        """Get score contribution (0.0 to 1.0)."""
        return {
            FitLevel.SATISFIED: 1.0,
            FitLevel.PARTIAL: 0.5,
            FitLevel.NOT_SATISFIED: 0.0,
        }[self]


class RecommendationLevel(Enum):
    """Final recommendation level."""

    PRIORITY = "priority"       # 🟢 80+ - Candidature prioritaire
    RECOMMENDED = "recommended"  # 🟢 60-79 - Candidature recommandée
    CONSIDER = "consider"       # 🟡 40-59 - À considérer
    RISKY = "risky"             # 🔴 < 40 - Profil peu adapté

    @property
    def emoji(self) -> str:
        """Get emoji representation."""
        return {
            RecommendationLevel.PRIORITY: "🟢",
            RecommendationLevel.RECOMMENDED: "🟢",
            RecommendationLevel.CONSIDER: "🟡",
            RecommendationLevel.RISKY: "🔴",
        }[self]

    @property
    def label(self) -> str:
        """Get display label."""
        return {
            RecommendationLevel.PRIORITY: "Candidature prioritaire",
            RecommendationLevel.RECOMMENDED: "Candidature recommandée",
            RecommendationLevel.CONSIDER: "À considérer selon motivation",
            RecommendationLevel.RISKY: "Profil peu adapté",
        }[self]

    @classmethod
    def from_score(cls, score: int) -> "RecommendationLevel":
        """Get recommendation level from score."""
        if score >= 80:
            return cls.PRIORITY
        if score >= 60:
            return cls.RECOMMENDED
        if score >= 40:
            return cls.CONSIDER
        return cls.RISKY


@dataclass(frozen=True)
class RequirementMatch:
    """A matched requirement with its fit level.

    CUPID: Idiomatic - uses frozen dataclass for immutability.
    """

    requirement: str
    level: FitLevel
    evidence: str = ""
    recommendation: str = ""

    @property
    def is_satisfied(self) -> bool:
        """Check if requirement is fully satisfied."""
        return self.level == FitLevel.SATISFIED

    @property
    def is_partial(self) -> bool:
        """Check if requirement is partially satisfied."""
        return self.level == FitLevel.PARTIAL

    @property
    def is_gap(self) -> bool:
        """Check if requirement is not satisfied."""
        return self.level == FitLevel.NOT_SATISFIED


@dataclass(frozen=True)
class TalkingPoint:
    """A talking point for the interview.

    CUPID: Domain-based - models interview preparation.
    """

    theme: str
    content: str
    related_requirement: str = ""


@dataclass(frozen=True)
class Strength:
    """A strength to highlight in the application.

    CUPID: Domain-based - models candidate strength.
    """

    title: str
    description: str
    evidence: str = ""


@dataclass(frozen=True)
class Gap:
    """A gap to address in the application.

    CUPID: Domain-based - models candidate gap.
    """

    title: str
    description: str
    strategy: str = ""


@dataclass(frozen=True)
class ScoreBreakdown:
    """Breakdown of the fit score by category.

    CUPID: Predictable - clear score decomposition.
    """

    must_have_score: float  # 0.0 to 1.0
    nice_to_have_score: float  # 0.0 to 1.0
    experience_score: float  # 0.0 to 1.0
    culture_score: float  # 0.0 to 1.0

    # Weights for each category
    MUST_HAVE_WEIGHT: float = 0.60
    NICE_TO_HAVE_WEIGHT: float = 0.20
    EXPERIENCE_WEIGHT: float = 0.15
    CULTURE_WEIGHT: float = 0.05

    @property
    def total_score(self) -> int:
        """Calculate total weighted score (0-100)."""
        weighted = (
            self.must_have_score * self.MUST_HAVE_WEIGHT +
            self.nice_to_have_score * self.NICE_TO_HAVE_WEIGHT +
            self.experience_score * self.EXPERIENCE_WEIGHT +
            self.culture_score * self.CULTURE_WEIGHT
        )
        return round(weighted * 100)

    @property
    def stars(self) -> str:
        """Get star rating based on score."""
        score = self.total_score
        if score >= 80:
            return "⭐⭐⭐⭐⭐"
        if score >= 60:
            return "⭐⭐⭐⭐☆"
        if score >= 40:
            return "⭐⭐⭐☆☆"
        if score >= 20:
            return "⭐⭐☆☆☆"
        return "⭐☆☆☆☆"

    @property
    def recommendation(self) -> RecommendationLevel:
        """Get recommendation level."""
        return RecommendationLevel.from_score(self.total_score)


@dataclass
class FitResult:
    """Complete result of a fit analysis.

    CUPID: Domain-based - the aggregate root of fit analysis domain.
    """

    job_title: str
    company: str
    score: ScoreBreakdown
    must_have_matches: list[RequirementMatch] = field(default_factory=list)
    nice_to_have_matches: list[RequirementMatch] = field(default_factory=list)
    strengths: list[Strength] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    talking_points: list[TalkingPoint] = field(default_factory=list)
    justification: str = ""

    @property
    def satisfied_must_haves(self) -> list[RequirementMatch]:
        """Get fully satisfied must-have requirements."""
        return [m for m in self.must_have_matches if m.is_satisfied]

    @property
    def partial_must_haves(self) -> list[RequirementMatch]:
        """Get partially satisfied must-have requirements."""
        return [m for m in self.must_have_matches if m.is_partial]

    @property
    def gap_must_haves(self) -> list[RequirementMatch]:
        """Get not satisfied must-have requirements."""
        return [m for m in self.must_have_matches if m.is_gap]

    @property
    def satisfied_nice_to_haves(self) -> list[RequirementMatch]:
        """Get fully satisfied nice-to-have requirements."""
        return [m for m in self.nice_to_have_matches if m.is_satisfied]

    @property
    def total_score(self) -> int:
        """Get total score."""
        return self.score.total_score

    @property
    def stars(self) -> str:
        """Get star rating."""
        return self.score.stars

    @property
    def recommendation(self) -> RecommendationLevel:
        """Get recommendation level."""
        return self.score.recommendation
