# Job-Analyze Workflow

Analyzes a job posting and extracts structured information.

## Usage

```bash
job-analyze [URL or job posting text]
```

**Accepted inputs:**

- URLs from LinkedIn, Welcome to the Jungle, Indeed, career sites
- Copy-pasted posting text

## Execution workflow

### Step 1: Fetch the content

**If a URL is provided:**

```text
1. Use WebFetch to retrieve the content
2. Parse the HTML/markdown
3. Extract the posting text
```

**If raw text is provided:**

```text
1. Use the text directly
```

### Step 2: Build the application ID

```text
Format: {company_slug}-{YYYY-MM-DD}
Example: google-2025-11-30
```

### Step 3: Extract structured information

**General information:**

- Job title
- Company
- Location
- Contract type (full-time, contract, freelance)
- Salary (if mentioned)
- Remote policy (if mentioned)

**Requirements:**

- **Must-have:** required skills / experience
- **Nice-to-have:** desired skills / experience

**Responsibilities:**

- List of primary missions

**ATS keywords:**

- Technologies mentioned
- Methodologies mentioned
- Soft skills requested
- Recurring terms

### Step 4: Company research (optional)

```text
1. WebSearch the company
2. Extract: industry, size, recent news
3. Identify the tech stack if possible
```

### Step 5: Flag points of attention

- Potential red flags (vague terms, unrealistic requirements)
- Positive signals (values, benefits, culture)

### Step 6: Generate the report

Create `data/applications/{app_id}/{app_id}-analysis.md`:

```markdown
# Analysis: {Job title} @ {Company}

**Analysis date:** {date}
**Source:** {url or "provided text"}

## General information

| Field | Value |
|-------|-------|
| **Role** | {title} |
| **Company** | {company} |
| **Location** | {location} |
| **Contract type** | {type} |
| **Salary** | {salary or "Not disclosed"} |
| **Remote** | {policy} |

## Requirements

### Mandatory (must-have)

- [ ] {skill 1}
- [ ] {skill 2}
- ...

### Desired (nice-to-have)

- [ ] {skill 1}
- [ ] {skill 2}
- ...

## Primary responsibilities

1. {responsibility 1}
2. {responsibility 2}
3. ...

## ATS keywords

`keyword1`, `keyword2`, `keyword3`, ...

## Company context

- **Industry:** {industry}
- **Size:** {size}
- **Recent news:** {news}

## Points of attention

### Positive signals

- {positive signal 1}
- {positive signal 2}

### Potential red flags

- {red flag 1} (if applicable)

## Recommendations for the application

- Emphasize: {key skills to highlight}
- Prepare: {questions/topics to anticipate}
```

### Step 7: Save the original posting

Create `data/applications/{app_id}/{app_id}-job-posting.md`:

```markdown
# Original posting

**Source:** {url}
**Captured on:** {date}

---

{full posting text}
```

## Output

### Generated files

```text
data/applications/{app_id}/
├── {app_id}-job-posting.md   # Original posting
└── {app_id}-analysis.md      # Structured analysis
```

### Confirmation message

```text
Job posting analysis complete.

Application ID: {app_id}
Role: {title} @ {company}
Location: {location}

Requirements identified:
- {n} must-have
- {n} nice-to-have

ATS keywords: {n} identified

Next step: job-fit to assess the fit
```

## Notes

- Keep the original posting for reference
- Checkboxes in the requirements list let `job-fit` track them
- ATS keywords feed `job-cv` for keyword optimization
