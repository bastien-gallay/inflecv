"""Regex patterns for job posting parsing.

CUPID: Unix philosophy - this module does ONE thing: define patterns.
All patterns are pure data, organized in namespace classes.
"""

from typing import Final


class SectionHeaders:
    """Headers for different job posting sections (FR/EN)."""

    REQUIREMENTS: Final[tuple[str, ...]] = (
        "Requirements",
        "Exigences",
        "Must-have",
        r"Compétences\s+techniques\s+recherchées",
        r"Profil\s+recherché",
        r"Required\s+Profile",
        r"Qualifications",
    )

    NICE_TO_HAVE: Final[tuple[str, ...]] = (
        "Nice-to-have",
        "Souhaité",
        "Optional",
        "Bonus",
        "Plus",
    )

    RESPONSIBILITIES: Final[tuple[str, ...]] = (
        "Responsibilities",
        "Responsabilités",
        r"Missions?\s+principales?",
        r"What you.ll do",
        "Your role",
        r"Description\s+du\s+poste",
    )


class SectionTerminators:
    """Patterns that indicate the end of a section."""

    REQUIREMENTS: Final[str] = (
        r"\n\n(?:[A-Z]|Compétences\s+humaines)|Compétences\s+humaines|\Z"
    )

    RESPONSIBILITIES: Final[str] = (
        r"\n\n(?:Profil|Modalités|Compétences)|Profil\s+recherché|\Z"
    )

    GENERIC: Final[str] = r"\n\n|\n[A-Z]|\Z"


class TechKeywords:
    """Technical keywords for ATS extraction."""

    PROGRAMMING_LANGUAGES: Final[tuple[str, ...]] = (
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
    )

    FRAMEWORKS: Final[tuple[str, ...]] = (
        "Django", "FastAPI", "Flask", "React", "Angular", "Vue",
        "Node.js", "Nodejs", "Spring", "Rails", "Next.js", "Nextjs",
    )

    DATABASES: Final[tuple[str, ...]] = (
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "SQL Server", "Oracle", "GraphQL",
    )

    CLOUD_PLATFORMS: Final[tuple[str, ...]] = (
        "AWS", "Azure", "GCP", "Kubernetes", "Docker", "Terraform",
    )

    AI_ML: Final[tuple[str, ...]] = (
        "Machine Learning", "ML", "AI", "Deep Learning",
        "PyTorch", "TensorFlow", "NLP", "Computer Vision",
    )

    METHODOLOGIES: Final[tuple[str, ...]] = (
        "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "TDD", "DDD",
    )

    COMPLIANCE: Final[tuple[str, ...]] = (
        "RGPD", "GDPR", "HDS", "SecNumCloud", "RGAA", "WCAG",
    )

    @classmethod
    def all_groups(cls) -> list[tuple[str, ...]]:
        """Return all keyword groups for iteration."""
        return [
            cls.PROGRAMMING_LANGUAGES,
            cls.FRAMEWORKS,
            cls.DATABASES,
            cls.CLOUD_PLATFORMS,
            cls.AI_ML,
            cls.METHODOLOGIES,
            cls.COMPLIANCE,
        ]


class LocationPatterns:
    """Patterns for location extraction."""

    FRENCH_CITIES: Final[tuple[str, ...]] = (
        "Paris", "Lyon", "Bordeaux", "Marseille", "Toulouse", "Nantes", "Nice",
    )

    KEYWORDS: Final[tuple[str, ...]] = (
        "Location", "Lieu", "Localisation",
        "basé", "based", "situé", "located",
    )


class ContractPatterns:
    """Patterns for contract type extraction."""

    TYPES: Final[tuple[str, ...]] = (
        "CDI", "CDD", "Freelance", "Stage", "Internship",
        "Full-time", "Part-time", "Temps plein", "Temps partiel",
    )


class RequirementMarkers:
    """Markers that indicate requirement type."""

    NICE_TO_HAVE: Final[tuple[str, ...]] = (
        r"nice.to.have",
        "souhaité",
        "optional",
        r"atout\s*:",
    )

    REQUIRED: Final[tuple[str, ...]] = (
        "required",
        "obligatoire",
    )


class TitlePatterns:
    """Patterns for title and company extraction."""

    SEPARATORS: Final[tuple[str, ...]] = (
        " - ",
        " @ ",
        " at ",
    )

    EXECUTIVE_TITLES: Final[tuple[str, ...]] = (
        "CTO", "CEO", "VP", "Director", "Lead",
    )


class Filters:
    """Patterns and terms to filter out."""

    KEYWORD_FALSE_POSITIVES: Final[frozenset[str]] = frozenset({
        "Technologies", "Inclusives", "Intelligence", "Artificielle",
        "The", "And", "For", "With", "From", "This", "That",
        "Nice",  # City vs "nice to have"
    })


