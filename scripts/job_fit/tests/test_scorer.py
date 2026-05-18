"""Tests for job_fit scorer."""

from scripts.job_fit.scorer import (
    calculate_fit_score,
    create_match,
    not_satisfied,
    partial,
    satisfied,
)
from scripts.job_fit.types import FitLevel


class TestCalculateFitScore:
    """Tests for calculate_fit_score function."""

    def test_empty_requirements(self) -> None:
        """Test score with no requirements."""
        score = calculate_fit_score([], [])
        # No requirements = 100% match on must-have and nice-to-have
        # 1.0 * 0.6 + 1.0 * 0.2 + 0.8 * 0.15 + 0.7 * 0.05
        # = 0.6 + 0.2 + 0.12 + 0.035 = 0.955 -> 96
        assert score.total_score == 96

    def test_all_satisfied(self) -> None:
        """Test score with all requirements satisfied."""
        must_haves = [
            satisfied("Python", "8 years"),
            satisfied("Leadership", "CTO experience"),
        ]
        nice_to_haves = [
            satisfied("TypeScript", "5 years"),
        ]
        score = calculate_fit_score(must_haves, nice_to_haves)
        # 1.0 * 0.6 + 1.0 * 0.2 + 0.8 * 0.15 + 0.7 * 0.05
        # = 0.6 + 0.2 + 0.12 + 0.035 = 0.955 -> 96
        assert score.total_score == 96
        assert score.must_have_score == 1.0
        assert score.nice_to_have_score == 1.0

    def test_all_not_satisfied(self) -> None:
        """Test score with no requirements satisfied."""
        must_haves = [
            not_satisfied("Go"),
            not_satisfied("Rust"),
        ]
        nice_to_haves = [
            not_satisfied("Kubernetes"),
        ]
        score = calculate_fit_score(must_haves, nice_to_haves)
        # 0.0 * 0.6 + 0.0 * 0.2 + 0.8 * 0.15 + 0.7 * 0.05
        # = 0.0 + 0.0 + 0.12 + 0.035 = 0.155 -> 16
        assert score.total_score == 16
        assert score.must_have_score == 0.0
        assert score.nice_to_have_score == 0.0

    def test_mixed_requirements(self) -> None:
        """Test score with mixed requirement satisfaction."""
        must_haves = [
            satisfied("Python", "8 years"),
            partial("Kubernetes", "Docker experience"),
            not_satisfied("AWS Certification"),
        ]
        # Average: (1.0 + 0.5 + 0.0) / 3 = 0.5
        score = calculate_fit_score(must_haves, [])
        assert score.must_have_score == 0.5

    def test_custom_experience_score(self) -> None:
        """Test with custom experience score."""
        score = calculate_fit_score([], [], experience_score=1.0)
        assert score.experience_score == 1.0

    def test_custom_culture_score(self) -> None:
        """Test with custom culture score."""
        score = calculate_fit_score([], [], culture_score=1.0)
        assert score.culture_score == 1.0


class TestCreateMatch:
    """Tests for create_match factory function."""

    def test_create_satisfied(self) -> None:
        """Test creating a satisfied match."""
        match = create_match("Python", FitLevel.SATISFIED, "8 years")
        assert match.requirement == "Python"
        assert match.level == FitLevel.SATISFIED
        assert match.evidence == "8 years"

    def test_create_partial(self) -> None:
        """Test creating a partial match."""
        match = create_match(
            "Kubernetes",
            FitLevel.PARTIAL,
            "Docker exp",
            "Mention learning",
        )
        assert match.requirement == "Kubernetes"
        assert match.level == FitLevel.PARTIAL
        assert match.evidence == "Docker exp"
        assert match.recommendation == "Mention learning"

    def test_create_not_satisfied(self) -> None:
        """Test creating a not satisfied match."""
        match = create_match(
            "AWS Cert",
            FitLevel.NOT_SATISFIED,
            recommendation="Highlight Azure experience",
        )
        assert match.requirement == "AWS Cert"
        assert match.level == FitLevel.NOT_SATISFIED
        assert match.recommendation == "Highlight Azure experience"


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_satisfied_function(self) -> None:
        """Test satisfied convenience function."""
        match = satisfied("Python", "8 years")
        assert match.level == FitLevel.SATISFIED
        assert match.evidence == "8 years"
        assert match.recommendation == ""

    def test_partial_function(self) -> None:
        """Test partial convenience function."""
        match = partial("Kubernetes", "Docker exp", "Mention learning")
        assert match.level == FitLevel.PARTIAL
        assert match.evidence == "Docker exp"
        assert match.recommendation == "Mention learning"

    def test_not_satisfied_function(self) -> None:
        """Test not_satisfied convenience function."""
        match = not_satisfied("AWS Cert", "Highlight Azure")
        assert match.level == FitLevel.NOT_SATISFIED
        assert match.evidence == ""
        assert match.recommendation == "Highlight Azure"
