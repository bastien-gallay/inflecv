"""Report generator for job posting analysis.

CUPID: Composable - each section builder is independent and testable.
"""

from .types import JobPosting


def _format_header(job: JobPosting) -> list[str]:
    """Format the report header."""
    return [
        f"# Analyse : {job.title} @ {job.company}",
        "",
    ]


def _format_info_section(job: JobPosting) -> list[str]:
    """Format general information section."""
    from .types import ContractType

    lines = [
        "## Informations générales",
        f"- **Poste**: {job.title}",
        f"- **Entreprise**: {job.company}",
    ]

    if job.location:
        lines.append(f"- **Localisation**: {job.location}")
    if job.contract_type != ContractType.UNKNOWN:
        lines.append(f"- **Type de contrat**: {job.contract_type.value}")
    if job.salary:
        lines.append(f"- **Salaire**: {job.salary}")

    lines.append("")
    return lines


def _format_requirements_section(job: JobPosting) -> list[str]:
    """Format requirements section with must-have and nice-to-have."""
    if not job.must_have and not job.nice_to_have:
        return []

    lines = ["## Exigences", ""]

    if job.must_have:
        lines.append(f"### Obligatoires ({len(job.must_have)})")
        lines.extend(f"- [ ] {req}" for req in job.must_have)
        lines.append("")

    if job.nice_to_have:
        lines.append(f"### Souhaitées ({len(job.nice_to_have)})")
        lines.extend(f"- [ ] {req}" for req in job.nice_to_have)
        lines.append("")

    return lines


def _format_responsibilities_section(job: JobPosting) -> list[str]:
    """Format responsibilities section."""
    if not job.responsibilities:
        return []

    lines = ["## Responsabilités principales"]
    lines.extend(f"{i}. {resp}" for i, resp in enumerate(job.responsibilities, 1))
    lines.append("")
    return lines


def _format_keywords_section(job: JobPosting) -> list[str]:
    """Format ATS keywords section."""
    if not job.keywords:
        return []

    return [
        "## Mots-clés ATS",
        f"`{'`, `'.join(job.keywords)}`",
        "",
    ]


def generate_report(job: JobPosting) -> str:
    """
    Generate a formatted analysis report for a job posting.

    CUPID: Composable - orchestrates independent section builders.

    Args:
        job: Parsed JobPosting object

    Returns:
        Formatted markdown report
    """
    sections = [
        _format_header(job),
        _format_info_section(job),
        _format_requirements_section(job),
        _format_responsibilities_section(job),
        _format_keywords_section(job),
    ]

    lines: list[str] = []
    for section in sections:
        lines.extend(section)

    return "\n".join(lines)
