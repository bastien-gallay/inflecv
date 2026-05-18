"""Tests for job_fit types."""

import pytest

from scripts.job_fit.types import (
    FitLevel,
    FitResult,
    Gap,
    RecommendationLevel,
    RequirementMatch,
    ScoreBreakdown,
    Strength,
    TalkingPoint,
)


class TestFitLevel:
    """Tests for FitLevel enum."""

    def test_emoji_satisfied(self) -> None:
        """Test emoji for satisfied level."""
        assert FitLevel.SATISFIED.emoji == "✅"

    def test_emoji_partial(self) -> None:
        """Test emoji for partial level."""
        assert FitLevel.PARTIAL.emoji == "⚠️"

    def test_emoji_not_satisfied(self) -> None:
        """Test emoji for not satisfied level."""
        assert FitLevel.NOT_SATISFIED.emoji == "❌"

    def test_score_satisfied(self) -> None:
        """Test score for satisfied level."""
        assert FitLevel.SATISFIED.score == 1.0

    def test_score_partial(self) -> None:
        """Test score for partial level."""
        assert FitLevel.PARTIAL.score == 0.5

    def test_score_not_satisfied(self) -> None:
        """Test score for not satisfied level."""
        assert FitLevel.NOT_SATISFIED.score == 0.0


class TestRecommendationLevel:
    """Tests for RecommendationLevel enum."""

    def test_from_score_priority(self) -> None:
        """Test priority recommendation for high scores."""
        assert RecommendationLevel.from_score(80) == RecommendationLevel.PRIORITY
        assert RecommendationLevel.from_score(100) == RecommendationLevel.PRIORITY

    def test_from_score_recommended(self) -> None:
        """Test recommended level for good scores."""
        assert RecommendationLevel.from_score(60) == RecommendationLevel.RECOMMENDED
        assert RecommendationLevel.from_score(79) == RecommendationLevel.RECOMMENDED

    def test_from_score_consider(self) -> None:
        """Test consider level for medium scores."""
        assert RecommendationLevel.from_score(40) == RecommendationLevel.CONSIDER
        assert RecommendationLevel.from_score(59) == RecommendationLevel.CONSIDER

    def test_from_score_risky(self) -> None:
        """Test risky level for low scores."""
        assert RecommendationLevel.from_score(0) == RecommendationLevel.RISKY
        assert RecommendationLevel.from_score(39) == RecommendationLevel.RISKY

    def test_emoji_priority(self) -> None:
        """Test emoji for priority level."""
        assert RecommendationLevel.PRIORITY.emoji == "🟢"

    def test_label_priority(self) -> None:
        """Test label for priority level."""
        assert RecommendationLevel.PRIORITY.label == "Candidature prioritaire"


class TestRequirementMatch:
    """Tests for RequirementMatch dataclass."""

    def test_is_satisfied(self) -> None:
        """Test is_satisfied property."""
        match = RequirementMatch("Python", FitLevel.SATISFIED, "8 years")
        assert match.is_satisfied
        assert not match.is_partial
        assert not match.is_gap

    def test_is_partial(self) -> None:
        """Test is_partial property."""
        match = RequirementMatch("Kubernetes", FitLevel.PARTIAL, "Docker exp")
        assert not match.is_satisfied
        assert match.is_partial
        assert not match.is_gap

    def test_is_gap(self) -> None:
        """Test is_gap property."""
        match = RequirementMatch("AWS Cert", FitLevel.NOT_SATISFIED)
        assert not match.is_satisfied
        assert not match.is_partial
        assert match.is_gap

    def test_immutability(self) -> None:
        """Test that RequirementMatch is immutable."""
        match = RequirementMatch("Python", FitLevel.SATISFIED)
        with pytest.raises(AttributeError):
            match.requirement = "Java"  # type: ignore


class TestScoreBreakdown:
    """Tests for ScoreBreakdown dataclass."""

    def test_total_score_all_perfect(self) -> None:
        """Test total score with all perfect scores."""
        score = ScoreBreakdown(1.0, 1.0, 1.0, 1.0)
        assert score.total_score == 100

    def test_total_score_all_zero(self) -> None:
        """Test total score with all zero scores."""
        score = ScoreBreakdown(0.0, 0.0, 0.0, 0.0)
        assert score.total_score == 0

    def test_total_score_mixed(self) -> None:
        """Test total score with mixed scores."""
        # 0.8 * 0.6 + 0.6 * 0.2 + 0.7 * 0.15 + 0.5 * 0.05
        # = 0.48 + 0.12 + 0.105 + 0.025 = 0.73 -> 73
        score = ScoreBreakdown(0.8, 0.6, 0.7, 0.5)
        assert score.total_score == 73

    def test_stars_excellent(self) -> None:
        """Test 5 stars for excellent score."""
        score = ScoreBreakdown(1.0, 1.0, 1.0, 1.0)
        assert score.stars == "⭐⭐⭐⭐⭐"

    def test_stars_good(self) -> None:
        """Test 4 stars for good score."""
        score = ScoreBreakdown(0.9, 0.7, 0.8, 0.7)  # ~82
        assert score.stars == "⭐⭐⭐⭐⭐"

    def test_stars_medium(self) -> None:
        """Test 3 stars for medium score."""
        score = ScoreBreakdown(0.5, 0.5, 0.5, 0.5)  # 50
        assert score.stars == "⭐⭐⭐☆☆"

    def test_recommendation(self) -> None:
        """Test recommendation from score."""
        score = ScoreBreakdown(1.0, 1.0, 1.0, 1.0)
        assert score.recommendation == RecommendationLevel.PRIORITY


class TestFitResult:
    """Tests for FitResult dataclass."""

    def test_satisfied_must_haves(self) -> None:
        """Test filtering satisfied must-haves."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(0.8, 0.6, 0.7, 0.5),
            must_have_matches=[
                RequirementMatch("Python", FitLevel.SATISFIED),
                RequirementMatch("Java", FitLevel.PARTIAL),
                RequirementMatch("Go", FitLevel.NOT_SATISFIED),
            ],
        )
        assert len(result.satisfied_must_haves) == 1
        assert result.satisfied_must_haves[0].requirement == "Python"

    def test_partial_must_haves(self) -> None:
        """Test filtering partial must-haves."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(0.8, 0.6, 0.7, 0.5),
            must_have_matches=[
                RequirementMatch("Python", FitLevel.SATISFIED),
                RequirementMatch("Java", FitLevel.PARTIAL),
            ],
        )
        assert len(result.partial_must_haves) == 1
        assert result.partial_must_haves[0].requirement == "Java"

    def test_gap_must_haves(self) -> None:
        """Test filtering gap must-haves."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(0.8, 0.6, 0.7, 0.5),
            must_have_matches=[
                RequirementMatch("Python", FitLevel.SATISFIED),
                RequirementMatch("Go", FitLevel.NOT_SATISFIED),
            ],
        )
        assert len(result.gap_must_haves) == 1
        assert result.gap_must_haves[0].requirement == "Go"

    def test_total_score_property(self) -> None:
        """Test total_score property delegates to score."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
        )
        assert result.total_score == 100

    def test_stars_property(self) -> None:
        """Test stars property delegates to score."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
        )
        assert result.stars == "⭐⭐⭐⭐⭐"

    def test_recommendation_property(self) -> None:
        """Test recommendation property delegates to score."""
        result = FitResult(
            job_title="Dev",
            company="TechCo",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
        )
        assert result.recommendation == RecommendationLevel.PRIORITY


class TestStrength:
    """Tests for Strength dataclass."""

    def test_creation(self) -> None:
        """Test Strength creation."""
        strength = Strength(
            title="Leadership",
            description="4 ans CTO",
            evidence="PALO IT 2021-2025",
        )
        assert strength.title == "Leadership"
        assert strength.description == "4 ans CTO"
        assert strength.evidence == "PALO IT 2021-2025"


class TestGap:
    """Tests for Gap dataclass."""

    def test_creation(self) -> None:
        """Test Gap creation."""
        gap = Gap(
            title="Certification AWS",
            description="Non certifié",
            strategy="Mettre en avant expérience Azure",
        )
        assert gap.title == "Certification AWS"
        assert gap.strategy == "Mettre en avant expérience Azure"


class TestTalkingPoint:
    """Tests for TalkingPoint dataclass."""

    def test_creation(self) -> None:
        """Test TalkingPoint creation."""
        tp = TalkingPoint(
            theme="Leadership",
            content="Mon expérience CTO démontre...",
            related_requirement="Management 50+ personnes",
        )
        assert tp.theme == "Leadership"
        assert tp.content == "Mon expérience CTO démontre..."
