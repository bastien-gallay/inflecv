"""Job fit analysis module.

Analyzes the fit between a candidate profile and job requirements.
"""

from .types import (
    FitLevel,
    FitResult,
    RequirementMatch,
    ScoreBreakdown,
    TalkingPoint,
)
from .scorer import calculate_fit_score
from .report import generate_fit_report

__all__ = [
    "FitLevel",
    "FitResult",
    "RequirementMatch",
    "ScoreBreakdown",
    "TalkingPoint",
    "calculate_fit_score",
    "generate_fit_report",
]
