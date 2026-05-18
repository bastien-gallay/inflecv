"""Fit score calculation.

CUPID:
- Composable: Uses RequirementMatch as building blocks
- Unix philosophy: Does one thing - calculates scores
- Predictable: Deterministic scoring from matches
- Idiomatic: Clean Python with type hints
- Domain-based: Returns domain object (ScoreBreakdown)
"""

from .types import FitLevel, RequirementMatch, ScoreBreakdown


def _calculate_match_ratio(matches: list[RequirementMatch]) -> float:
    """Calculate match ratio from a list of requirement matches.

    Args:
        matches: List of requirement matches

    Returns:
        Float between 0.0 and 1.0 representing match ratio
    """
    if not matches:
        return 1.0  # No requirements = 100% match

    total_score = sum(m.level.score for m in matches)
    return total_score / len(matches)


def calculate_fit_score(
    must_have_matches: list[RequirementMatch],
    nice_to_have_matches: list[RequirementMatch],
    experience_score: float = 0.8,
    culture_score: float = 0.7,
) -> ScoreBreakdown:
    """Calculate the overall fit score.

    Args:
        must_have_matches: List of must-have requirement matches
        nice_to_have_matches: List of nice-to-have requirement matches
        experience_score: Score for experience relevance (0.0 to 1.0)
        culture_score: Score for cultural fit (0.0 to 1.0)

    Returns:
        ScoreBreakdown with all component scores

    Example:
        >>> matches = [
        ...     RequirementMatch("Python", FitLevel.SATISFIED, "8 years"),
        ...     RequirementMatch("Kubernetes", FitLevel.PARTIAL, "Docker exp"),
        ... ]
        >>> score = calculate_fit_score(matches, [])
        >>> print(score.total_score)
        62
    """
    must_have_ratio = _calculate_match_ratio(must_have_matches)
    nice_to_have_ratio = _calculate_match_ratio(nice_to_have_matches)

    return ScoreBreakdown(
        must_have_score=must_have_ratio,
        nice_to_have_score=nice_to_have_ratio,
        experience_score=experience_score,
        culture_score=culture_score,
    )


def create_match(
    requirement: str,
    level: FitLevel,
    evidence: str = "",
    recommendation: str = "",
) -> RequirementMatch:
    """Factory function to create a RequirementMatch.

    Args:
        requirement: The requirement text
        level: The fit level (SATISFIED, PARTIAL, NOT_SATISFIED)
        evidence: Evidence from the profile
        recommendation: Strategy to address the gap

    Returns:
        RequirementMatch object
    """
    return RequirementMatch(
        requirement=requirement,
        level=level,
        evidence=evidence,
        recommendation=recommendation,
    )


def satisfied(requirement: str, evidence: str = "") -> RequirementMatch:
    """Create a satisfied requirement match.

    Args:
        requirement: The requirement text
        evidence: Evidence from the profile

    Returns:
        RequirementMatch with SATISFIED level
    """
    return create_match(requirement, FitLevel.SATISFIED, evidence)


def partial(
    requirement: str,
    evidence: str = "",
    recommendation: str = "",
) -> RequirementMatch:
    """Create a partially satisfied requirement match.

    Args:
        requirement: The requirement text
        evidence: Evidence from the profile
        recommendation: Strategy to address the gap

    Returns:
        RequirementMatch with PARTIAL level
    """
    return create_match(requirement, FitLevel.PARTIAL, evidence, recommendation)


def not_satisfied(
    requirement: str,
    recommendation: str = "",
) -> RequirementMatch:
    """Create a not satisfied requirement match.

    Args:
        requirement: The requirement text
        recommendation: Strategy to address the gap

    Returns:
        RequirementMatch with NOT_SATISFIED level
    """
    return create_match(requirement, FitLevel.NOT_SATISFIED, "", recommendation)
