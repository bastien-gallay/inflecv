"""Report generator for job fit analysis.

CUPID: Composable - each section builder is independent and testable.
"""

from .types import FitResult, RequirementMatch


def _format_header(result: FitResult) -> list[str]:
    """Format the report header with score."""
    return [
        f"# Adéquation : {result.job_title} @ {result.company}",
        "",
        f"## Score global : {result.total_score}/100 {result.stars}",
        "",
    ]


def _format_satisfied_section(matches: list[RequirementMatch], is_must_have: bool) -> list[str]:
    """Format the satisfied requirements section."""
    satisfied = [m for m in matches if m.is_satisfied]
    if not satisfied:
        return []

    label = "obligatoires" if is_must_have else "souhaitées"
    lines = [
        f"### ✅ Exigences {label} satisfaites ({len(satisfied)}/{len(matches)})",
        "",
        "| Exigence | Preuve dans le profil |",
        "|----------|----------------------|",
    ]
    for m in satisfied:
        evidence = m.evidence or "-"
        lines.append(f"| {m.requirement} | {evidence} |")
    lines.append("")
    return lines


def _format_partial_section(matches: list[RequirementMatch]) -> list[str]:
    """Format the partially satisfied requirements section."""
    partial = [m for m in matches if m.is_partial]
    if not partial:
        return []

    lines = [
        f"### ⚠️ Exigences partiellement satisfaites ({len(partial)}/{len(matches)})",
        "",
        "| Exigence | Situation actuelle | Recommandation |",
        "|----------|-------------------|----------------|",
    ]
    for m in partial:
        evidence = m.evidence or "-"
        recommendation = m.recommendation or "-"
        lines.append(f"| {m.requirement} | {evidence} | {recommendation} |")
    lines.append("")
    return lines


def _format_gap_section(matches: list[RequirementMatch]) -> list[str]:
    """Format the not satisfied requirements section."""
    gaps = [m for m in matches if m.is_gap]
    if not gaps:
        return []

    lines = [
        f"### ❌ Exigences non satisfaites ({len(gaps)}/{len(matches)})",
        "",
        "| Exigence | Impact | Stratégie |",
        "|----------|--------|-----------|",
    ]
    for m in gaps:
        recommendation = m.recommendation or "-"
        lines.append(f"| {m.requirement} | Moyen | {recommendation} |")
    lines.append("")
    return lines


def _format_requirements_section(result: FitResult) -> list[str]:
    """Format the complete requirements section."""
    lines = ["## Correspondance des exigences", ""]

    # Must-have requirements
    if result.must_have_matches:
        lines.extend(_format_satisfied_section(result.must_have_matches, is_must_have=True))
        lines.extend(_format_partial_section(result.must_have_matches))
        lines.extend(_format_gap_section(result.must_have_matches))

    # Nice-to-have requirements
    if result.nice_to_have_matches:
        lines.extend(_format_satisfied_section(result.nice_to_have_matches, is_must_have=False))

    return lines


def _format_strengths_section(result: FitResult) -> list[str]:
    """Format the strengths section."""
    if not result.strengths:
        return []

    lines = ["## Points forts à valoriser", ""]
    for i, s in enumerate(result.strengths, 1):
        lines.append(f"{i}. **{s.title}** : {s.description}")
    lines.append("")
    return lines


def _format_gaps_section(result: FitResult) -> list[str]:
    """Format the gaps section."""
    if not result.gaps:
        return []

    lines = ["## Lacunes à adresser", ""]
    for i, g in enumerate(result.gaps, 1):
        strategy = f" - {g.strategy}" if g.strategy else ""
        lines.append(f"{i}. **{g.title}** : {g.description}{strategy}")
    lines.append("")
    return lines


def _format_talking_points_section(result: FitResult) -> list[str]:
    """Format the talking points section."""
    if not result.talking_points:
        return []

    lines = ["## Talking points pour l'entretien", ""]
    for tp in result.talking_points:
        lines.append(f"- \"{tp.content}\"")
    lines.append("")
    return lines


def _format_recommendation_section(result: FitResult) -> list[str]:
    """Format the final recommendation section."""
    rec = result.recommendation
    lines = [
        "## Recommandation finale",
        "",
        f"{rec.emoji} **{rec.label}**",
        "",
        f"**Score** : {result.total_score}/100",
        "",
    ]
    if result.justification:
        lines.extend([
            f"**Justification** : {result.justification}",
            "",
        ])
    return lines


def generate_fit_report(result: FitResult) -> str:
    """Generate a formatted fit analysis report.

    CUPID: Composable - orchestrates independent section builders.

    Args:
        result: FitResult object with all analysis data

    Returns:
        Formatted markdown report
    """
    sections = [
        _format_header(result),
        _format_requirements_section(result),
        _format_strengths_section(result),
        _format_gaps_section(result),
        _format_talking_points_section(result),
        _format_recommendation_section(result),
    ]

    lines: list[str] = []
    for section in sections:
        lines.extend(section)

    return "\n".join(lines)
