---
name: job-application
description: Job offer analysis, profile/role fit assessment, and tailored CV/cover letter generation. Activate this skill when the user mentions a job application, a job posting, a cover letter, or an adapted CV.
version: 1.1.0
commands:
  - job-analyze
  - job-fit
  - job-cv
  - job-letter
---

# Job Application Skill

Assistant for the job application process: posting analysis, fit
assessment, tailored CV and cover letter generation.

## Available Commands

### job-analyze

Analyzes a job posting and extracts structured information.

```bash
job-analyze [URL or job posting text]
```

**Features:**

- Parses the posting from a URL (LinkedIn, WTTJ, Indeed) or raw text
- Extracts mandatory vs nice-to-have requirements
- Identifies ATS keywords
- Looks up company information (optional)
- Generates a structured analysis report

See [workflows/job-analyze.md](workflows/job-analyze.md) for details.

### job-fit

Analyzes the fit between profile and role, with interactive validation.

```bash
job-fit [--application=ID]
```

**Features:**

- Compares the CV against the posting's requirements
- Computes an overall fit score (0-100)
- Identifies strengths and gaps
- Generates interview talking points
- **Validation questionnaire** (AskUserQuestion or text fallback)
- **Confirmation before CV generation** (stop possible if fit is too low)
- Provides a go/no-go recommendation

See [workflows/job-fit.md](workflows/job-fit.md) for details.

### job-cv

Generates a CV tailored to the job posting via an interactive questionnaire.

```bash
job-cv [--format=short|long] [--dry-run]
```

**Features:**

- **Format mirrors the posting** (short → short CV, long → long CV)
- **Customization questionnaire** (title, ordering, experiences, keywords, sidebar)
- Reorders experiences by relevance
- Injects ATS keywords from the posting
- Adjusts sidebar skills
- Generates the tailored Typst source with **document metadata**
- Compiles the PDF automatically
- **Visual check** post-compilation (pages, blank areas, overflows)
- Produces a report of the modifications

See [workflows/job-cv.md](workflows/job-cv.md) for details.

### job-letter (Planned - INF-011)

Generates a personalized cover letter.

```bash
job-letter [--style=formal|modern]
```

## Architecture

```text
.claude/skills/job-application/
├── SKILL.md                    # This file (Level 1)
├── workflows/                  # Detailed instructions (Level 2)
│   ├── job-analyze.md
│   ├── job-fit.md
│   ├── job-cv.md
│   └── job-letter.md
└── templates/                  # Output templates
    └── cv-adapted-template.typ

data/applications/              # Per-application data
└── {app_id}/                   # Format: {company-slug}-{YYYY-MM-DD}
    ├── {app_id}-job-posting.md     # Original posting
    ├── {app_id}-analysis.md        # job-analyze output
    ├── {app_id}-fit-report.md      # job-fit output (validated)
    ├── {app_id}-modifications.md   # User choices for job-cv
    ├── {app_id}-cv-adapted.typ     # Adapted CV (Typst source)
    └── {app_id}-cv-adapted.pdf     # Compiled PDF
```

## Typical workflow

```text
     [Job posting]
            |
            v
    +---------------+
    | job-analyze   |  --> {app_id}-analysis.md
    +---------------+
            |
            v
    +---------------+
    | job-fit       |  --> {app_id}-fit-report.md
    +---------------+        |
            |                v
            |         [Validation questionnaire]
            |                |
            |          +-----+-----+
            |          |           |
            |     [Continue]    [Stop]
            |          |           |
            |          v           v
            |    +----------+   [END]
            |    | job-cv   |
            |    +----------+
            |          |
            |          v
            |    [Customization questionnaire]
            |          |
            |          v
            |    [Generation + Compilation]
            |          |
            |          v
            |    [Visual check]
            |          |
            v          v
+-----------+    [Adapted CV]
| job-letter|
+-----------+
      |
      v
  [Cover letter]
```

## Data model

```yaml
application:
  id: "{company-slug}-{date}"      # e.g. wavestone-2025-11-30
  job:
    title: string
    company: string
    location: string
    type: string                   # full-time, contract, freelance
    url: string
    word_count: number             # Used to choose CV format
    company_type: string           # startup, large_group, consulting
    requirements:
      must_have: []
      nice_to_have: []
    responsibilities: []
    keywords: []                   # ATS keywords
  fit_analysis:
    score: number                  # 0-100
    strengths: []
    gaps: []
    talking_points: []
    recommendation: string         # go/consider/no-go
    validated: boolean             # User validation
  cv_customization:
    format: string                 # short/long
    title: string                  # Adapted title
    experiences_order: []          # Custom order
    experiences_omit: []           # Experiences to omit
    keywords_priority: string      # all/selection
    sidebar_order: string          # auto/manual
  outputs:
    cv_adapted: path
    cover_letter: path
```

## File naming

All files use the `{app_id}` prefix (application slug):

| File | Description |
|------|-------------|
| `{app_id}-job-posting.md` | Original posting, saved verbatim |
| `{app_id}-analysis.md` | Structured analysis of the posting |
| `{app_id}-fit-report.md` | Validated fit report |
| `{app_id}-modifications.md` | User choices for the CV |
| `{app_id}-cv-adapted.typ` | Typst source of the adapted CV |
| `{app_id}-cv-adapted.pdf` | Compiled PDF |

## Compilation

```bash
# Compile an adapted CV
just build-adapted {app_id}

# Example
just build-adapted wavestone-2025-11-30
```

## Links

- **CV Source:** [src/cv.typ](../../../src/cv.typ)
- **CV Short:** [src/cv-short.typ](../../../src/cv-short.typ)
- **CV Modules:** [src/shared/](../../../src/shared/)
- **Applications Data:** [data/applications/](../../../data/applications/)

---

**Version:** 1.1.0
**Last Updated:** 2026-05-16
