"""Company research module - provides structured prompts for WebSearch integration."""

from dataclasses import dataclass


@dataclass
class CompanyResearchPrompt:
    """Structured prompt for company research via WebSearch."""

    company: str
    queries: list[str]
    analysis_prompt: str


def create_company_research_prompt(company: str, sector: str | None = None) -> CompanyResearchPrompt:
    """
    Create structured prompts for researching a company.

    Args:
        company: Company name to research
        sector: Optional sector hint (e.g., "EdTech", "HealthTech")

    Returns:
        CompanyResearchPrompt with queries and analysis prompt
    """
    base_queries = [
        f"{company} entreprise taille employés",
        f"{company} avis salariés Glassdoor",
        f"{company} actualités levée de fonds",
    ]

    if sector:
        base_queries.append(f"{company} {sector} innovation")

    analysis_prompt = f"""Analyse les informations sur l'entreprise {company}.

Extrais et structure les informations suivantes :

## Informations générales
- **Secteur d'activité** : [secteur principal]
- **Taille** : [nombre d'employés ou fourchette]
- **Localisation** : [siège social]
- **Date de création** : [année si disponible]
- **Statut** : [startup, scale-up, PME, grand groupe]

## Financement
- **Dernière levée** : [montant et date si disponible]
- **Investisseurs** : [principaux investisseurs]
- **Valorisation** : [si disponible]

## Culture et réputation
- **Note Glassdoor** : [note /5 si disponible]
- **Points positifs** : [2-3 points mentionnés par les employés]
- **Points d'attention** : [2-3 points à surveiller]

## Actualités récentes
- [Actualité 1]
- [Actualité 2]

## Analyse pour la candidature
- **Atouts à mettre en avant** : [compétences pertinentes pour cette entreprise]
- **Questions à préparer** : [questions pertinentes pour l'entretien]
"""

    return CompanyResearchPrompt(
        company=company,
        queries=base_queries,
        analysis_prompt=analysis_prompt,
    )


def format_company_section(
    company: str,
    sector: str | None = None,
    size: str | None = None,
    funding: str | None = None,
    glassdoor_rating: float | None = None,
    highlights: list[str] | None = None,
    concerns: list[str] | None = None,
) -> str:
    """
    Format company research results into a markdown section.

    Args:
        company: Company name
        sector: Business sector
        size: Company size (employees)
        funding: Recent funding info
        glassdoor_rating: Rating out of 5
        highlights: Positive points
        concerns: Points of attention

    Returns:
        Formatted markdown section
    """
    lines = ["## Contexte entreprise", ""]

    if sector:
        lines.append(f"- **Secteur** : {sector}")
    if size:
        lines.append(f"- **Taille** : {size}")
    if funding:
        lines.append(f"- **Financement** : {funding}")
    if glassdoor_rating:
        lines.append(f"- **Note Glassdoor** : {glassdoor_rating}/5")

    if highlights:
        lines.append("")
        lines.append("### Points positifs")
        for h in highlights:
            lines.append(f"- ✅ {h}")

    if concerns:
        lines.append("")
        lines.append("### Points d'attention")
        for c in concerns:
            lines.append(f"- ⚠️ {c}")

    lines.append("")
    return "\n".join(lines)
