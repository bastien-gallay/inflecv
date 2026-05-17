# Job-CV Workflow

Generates a CV tailored to a specific job posting via an interactive questionnaire.

## Usage

```bash
job-cv [--format=short|long] [--dry-run] [--application=ID]
```

**Options:**

- `--format`: short version (1 page) or long version (2+ pages). Default: mirror the posting
- `--dry-run`: print modifications without generating files
- `--application`: specific application ID. Default: most recent analysis

## Prerequisites

1. A posting analysis must exist (`job-analyze`)
2. A fit analysis must exist and be validated (`job-fit`)

## Execution workflow

### Step 1: Load the data

```text
Load:
- data/applications/{app_id}/{app_id}-analysis.md
- data/applications/{app_id}/{app_id}-fit-report.md

Extract:
- keywords: list of ATS keywords
- requirements: must-have and nice-to-have
- strengths: identified strengths
- gaps: identified gaps
- job_word_count: posting word count
- company_type: company type (startup, large group, consultancy)
```

### Step 2: Recommend the CV format (mirror the posting)

**Recommendation logic:**

| Posting criterion | Recommended format |
|-------------------|--------------------|
| < 500 words | Short (1 page) |
| > 500 words | Long (2+ pages) |
| Startup, scale-up | Short |
| Large group, consultancy | Long |
| "Detailed CV requested" | Long |
| Spontaneous application | Short |

**Confirmation question:**

```json
{
  "question": "The posting looks {short/long}. I recommend the {short/long} format. Confirm?",
  "header": "CV format",
  "multiSelect": false,
  "options": ["Yes, {short/long} format", "No, {long/short} format", "Other: free text"]
}
```

**Text fallback:**

```text
Recommended CV format

The posting looks {short/long} ({n} words, {company_type}).
I recommend the {short/long} format.

1. Yes, {short/long} format
2. No, {long/short} format
3. Other (specify)
```

### Step 3: Customization questionnaire

**Q1 - Job title:**

```json
{
  "question": "Which title to display on the CV?",
  "header": "Title",
  "multiSelect": false,
  "options": ["Keep: {current_title}", "Adapt: {suggestion_from_posting}", "Other: free text"]
}
```

**Q2 - Experience ordering:**

```json
{
  "question": "How to order experiences?",
  "header": "Order",
  "multiSelect": false,
  "options": ["Automatic (by relevance)", "Reverse chronological", "Other: free text"]
}
```

**Q3 - Experiences to omit:**

```json
{
  "question": "Any experiences to omit?",
  "header": "Omit",
  "multiSelect": true,
  "options": ["None", "{exp_1_name}", "{exp_2_name}", "Other: free text"]
}
```

**Q4 - ATS keywords:**

```json
{
  "question": "Which ATS keywords to prioritize?",
  "header": "Keywords",
  "multiSelect": false,
  "options": ["All identified keywords", "Manual selection...", "Other: free text"]
}
```

**Q5 - Sidebar:**

```json
{
  "question": "How to adapt the sidebar?",
  "header": "Sidebar",
  "multiSelect": false,
  "options": ["Automatic (reorder by relevance)", "Keep current order", "Other: free text"]
}
```

**Text fallback:**

```text
CV customization

1. Job title?
   a) Keep: "{current_title}"
   b) Adapt: "{suggestion}"
   c) Other (specify)

2. Experience ordering?
   a) Automatic (by relevance)
   b) Reverse chronological
   c) Other (specify)

3. Experiences to omit?
   a) None
   b) List (specify)

4. ATS keywords?
   a) All identified keywords
   b) Manual selection (specify)

5. Sidebar?
   a) Automatic (reorder)
   b) Keep current order

Answer with letters or describe.
```

### Step 4: Save the choices

Create / update `data/applications/{app_id}/{app_id}-modifications.md`:

```markdown
# CV modifications: {job_title} @ {company}

**Date:** {date}
**Chosen format:** {short|long}

## User choices

- **Title:** {choice}
- **Experience ordering:** {choice}
- **Omitted experiences:** {choice}
- **ATS keywords:** {choice}
- **Sidebar:** {choice}

## Applied adaptations

{details of modifications}
```

### Step 5: Compute the adaptations

```text
adaptations = {
    experiences_order: [exp ranked by relevance],
    experiences_detail: {exp_name: level},
    experiences_omit: [exp to omit],
    sidebar_skills: [skills reordered],
    about_text: "adapted text",
    keywords_to_inject: [prioritized keywords],
    format: "short" | "long",
    title: "adapted title",
}
```

### Step 6: Generate the Typst file

Create `data/applications/{app_id}/{app_id}-cv-adapted.typ`:

```typst
// CV adapted for: {job_title} @ {company}
// Date: {date}
// Fit score: {score}/100

#import "../../../src/neat-cv-local.typ": (...)
#import "../../../src/shared/config.typ": *
#import "../../../src/shared/experiences.typ": *
#import "../../../src/shared/sections.typ": *

// Document metadata
#set document(
  title: "CV - {Firstname} {Lastname} - {Position} @ {Company}",
  author: "{Firstname} {Lastname}",
  date: datetime.today(),
)

// Adapted configuration
#let author-adapted = (
  ..author-config,
  position: "{adapted_position}",
)

// Adapted sidebar
#let sidebar-adapted() = [
  = About
  {about_text_adapted}

  // ... reordered sections
]

// Adapted experiences
#let experiences-adapted = [
  = Professional Experience

  // Experiences in the new order
]

// Document
#show: cv-setup.with(author: author-adapted, ...)
#cv-page-one(
  profile-picture: image("../../../src/assets/photo-profile-pro.jpg"),
  sidebar-adapted(),
  [#experiences-adapted ...]
)
```

**Important — relative paths:**

- The file lives under `data/applications/{app_id}/`
- Imports must use `../../../src/` (3 levels up)

### Step 7: Compile the PDF

```bash
just build-adapted {app_id}
```

### Step 8: Visual check

Read the generated PDF and verify:

1. **Page count:** matches the chosen format (1 for short, 2+ for long)
2. **No extra page:** no nearly-empty final page
3. **Blank areas:** no large blank zone at the end of a column or page
4. **Readability:** no truncated or overflowing text
5. **Consistency:** sections are complete

**If a problem is detected:**

```text
Problem detected in the generated CV:

- Type: {overflow|blank_area|extra_page|...}
- Location: {page X, section Y}
- Description: {details}

Proposed action:
- {adjust content|change format|reduce experiences|...}

Would you like me to apply this fix?
```

Regenerate if needed.

## Adaptation rules

### 1. Experience reordering

**Principle:** put the most role-relevant experiences first.

**Scoring algorithm:**

```text
For each experience:
  score = 0
  score += keywords_match(exp, job.keywords) * 3      # ATS keywords
  score += skills_match(exp, job.requirements) * 2    # Required skills
  score += domain_match(exp, job.industry)            # Industry domain
  score += recency_bonus(exp.end_date)                # Recency bonus

Reorder by descending score
```

**Available experiences (src/shared/experiences.typ):**

| Variable | Role | Period | Relevance type |
|----------|------|--------|----------------|
| `exp-palo-it` | CTO @ PALO IT | 2021-2025 | Tech, AI, Management |
| `exp-upwiser` | Agile Coach @ Upwiser | 2013-2021 | Agile, Coaching, Startups |
| `exp-cdiscount` | Project Lead @ CDiscount | 2010-2013 | E-commerce, Payments |
| `exp-cast` | Consultant @ Cast | 2006-2010 | Consulting, Project mgmt |
| `exp-dev-web` | Web Dev @ Boonty | 2002-2006 | Development |

### 2. Detail-level adjustment

| Relevance | Detail level | Actions |
|-----------|--------------|---------|
| Very high | Expanded | Add bullets, numbers, tech stack |
| High | Standard | Keep as is |
| Medium | Condensed | Reduce to 2-3 essential bullets |
| Low | Minimal | One line or omit |

### 3. ATS optimization (keywords)

**Keyword sources:**

- `{app_id}-analysis.md` > "ATS keywords" section
- `{app_id}-fit-report.md` > "Met requirements" section

**Injection rules:**

1. **Priority 1 - Titles:** include in the job title if relevant
2. **Priority 2 - Bullets:** rephrase to include the exact terms
3. **Priority 3 - Sidebar:** reorder requested skills to the front

**Constraints:**

- Never add skills you don't have
- Keep the language natural (no keyword stuffing)
- Maximum 5-7 keywords added per section

### 4. Sidebar adaptation

| Section | Possible adaptation |
|---------|---------------------|
| About | Rephrase for the target role |
| Leadership | Reorder pills by relevance |
| Tech & AI | Reorder, add/remove pills |
| Methodology | Reorder based on context |

## Output

### Generated files

```text
data/applications/{app_id}/
├── {app_id}-modifications.md    # User choices and modifications
├── {app_id}-cv-adapted.typ      # Adapted Typst source
└── {app_id}-cv-adapted.pdf      # Compiled and verified PDF
```

### Confirmation message

```text
Adapted CV generated successfully.

Role: {job_title} @ {company}
Format: {short|long} ({n} pages)
Fit score: {score}/100

Main modifications:
- {n} experiences reordered
- {n} ATS keywords injected
- Sidebar adapted

Visual check: OK

Files:
- [{app_id}-cv-adapted.pdf](data/applications/{app_id}/{app_id}-cv-adapted.pdf)

Review the CV before sending.
```

## Important notes

1. **Always review** the generated CV before sending
2. **Never misrepresent** skills or experience
3. **Stay consistent** with the source CV
4. **Document** modifications for traceability
5. **Visual check** systematic after compilation
