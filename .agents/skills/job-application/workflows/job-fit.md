# Job-Fit Workflow

Analyzes the fit between profile and role with interactive validation.

## Usage

```bash
job-fit [--application=ID]
```

**Options:**

- `--application`: application ID. Default: most recent analysis

## Prerequisites

A posting analysis must exist (`job-analyze`).

## Execution workflow

### Step 1: Load the data

```text
1. Load data/applications/{app_id}/{app_id}-analysis.md
2. Load the CV source (src/cv.typ + modules under shared/)
3. Extract skills and experiences from the profile
```

### Step 2: Compare requirements

**For each must-have requirement:**

```text
Possible status:
- Met: clear evidence in the profile
- Partially met: closely related skill or being acquired
- Not met: no evidence in the profile
```

**For each nice-to-have requirement:**

```text
Same logic, but lower weight in the score
```

### Step 3: Compute the fit score

```text
score = (
    must_have_match * 0.60 +      # 60% weight on mandatory requirements
    nice_to_have_match * 0.20 +   # 20% weight on desired requirements
    experience_relevance * 0.15 + # 15% experience relevance
    culture_fit * 0.05            # 5% culture fit
) * 100

Round to the nearest integer
```

**Interpretation:**

| Score | Level | Recommendation |
|-------|-------|----------------|
| 80-100 | Excellent | Priority application |
| 60-79 | Good | Recommended |
| 40-59 | Average | Evaluate based on motivation |
| 0-39 | Low | Risky application |

### Step 4: Identify strengths and gaps

**Strengths:**

- Skills that match exactly
- Highly relevant experience
- Required certifications you already hold

**Gaps:**

- Unmet requirements
- Experience shortfalls
- Technologies not yet mastered

### Step 5: Generate talking points

For each strength / gap, prepare an argument:

```text
Strength: "My experience with X demonstrates that..."
Gap: "Although I don't have Y, my experience with Z is transferable because..."
```

### Step 6: Generate the initial report

Create `data/applications/{app_id}/{app_id}-fit-report.md`:

```markdown
# Fit: {Job title} @ {Company}

**Analysis date:** {date}
**Overall score:** {score}/100

## Summary

{2-3 sentence summary of the fit}

## Requirement match

### Met requirements ({n}/{total})

| Requirement | Evidence in the profile |
|-------------|--------------------------|
| {requirement} | {experience/skill that proves it} |
| ... | ... |

### Partially met requirements ({n}/{total})

| Requirement | Current state | Recommendation |
|-------------|--------------|----------------|
| {requirement} | {current state} | {how to compensate} |
| ... | ... | ... |

### Unmet requirements ({n}/{total})

| Requirement | Impact | Strategy |
|-------------|--------|----------|
| {requirement} | {Low/Medium/High} | {how to address} |
| ... | ... | ... |

## Strengths to highlight

1. **{title}:** {description and evidence}
2. **{title}:** {description and evidence}
3. ...

## Gaps to address

1. **{gap}:** {strategy to compensate}
2. **{gap}:** {strategy to compensate}
3. ...

## Interview talking points

### Highlighting strengths

- "{opening line for strength 1}"
- "{opening line for strength 2}"

### Addressing gaps

- "{prepared answer for gap 1}"
- "{prepared answer for gap 2}"

## Final recommendation

{go|consider|no-go} Application {recommended|to consider|poorly suited}

**Rationale:** {main reason}

## Suggested next steps

- [ ] Adapt the CV with job-cv
- [ ] Prepare the cover letter with job-letter
- [ ] {other action if relevant}
```

### Step 7: Show the link to the report

```text
Report generated: [{app_id}-fit-report.md](data/applications/{app_id}/{app_id}-fit-report.md)

Please review the report before validating.
```

### Step 8: Interactive validation (AskUserQuestion)

**Q1 - Must-have requirements:**

```json
{
  "question": "Are the must-have requirements correctly identified?",
  "header": "Must-have",
  "multiSelect": false,
  "options": ["Yes", "No, missing...", "Other: free text"]
}
```

**Q2 - Strengths:**

```json
{
  "question": "Are the strengths properly highlighted?",
  "header": "Strengths",
  "multiSelect": false,
  "options": ["Yes", "Add...", "Other: free text"]
}
```

**Q3 - Gaps:**

```json
{
  "question": "Are there any unmentioned gaps?",
  "header": "Gaps",
  "multiSelect": false,
  "options": ["No", "Yes...", "Other: free text"]
}
```

**Q4 - Score:**

```json
{
  "question": "Is the fit score correct?",
  "header": "Score",
  "multiSelect": false,
  "options": ["Correct", "Too high", "Too low", "Other: free text"]
}
```

**Text fallback (if AskUserQuestion is unavailable):**

```text
Please validate the report:

1. Are the must-have requirements correctly identified?
   a) Yes
   b) No, missing...

2. Are the strengths properly highlighted?
   a) Yes
   b) Add...

3. Are there any unmentioned gaps?
   a) No
   b) Yes...

4. Is the fit score correct?
   a) Correct
   b) Too high
   c) Too low

Answer with letters (e.g. "1a, 2a, 3a, 4a") or describe your corrections.
```

### Step 9: Update the report

If the user provided corrections:

1. Edit `{app_id}-fit-report.md` with the corrections
2. Recompute the score if needed
3. Show the changes made

### Step 10: Confirmation to continue

**Confirmation question:**

```json
{
  "question": "Continue with CV generation?",
  "header": "Continue?",
  "multiSelect": false,
  "options": ["Yes, continue", "No, stop (fit too low)"]
}
```

**Text fallback:**

```text
Continue with CV generation?
1. Yes, continue
2. No, stop (fit too low)
```

**If "No, stop":**

```text
Workflow stopped by the user.

Reason: Fit judged too low for this application.
Score: {score}/100

The fit report is still available:
[{app_id}-fit-report.md](data/applications/{app_id}/{app_id}-fit-report.md)

You can resume the process later with:
job-fit --application={app_id}
```

**END OF WORKFLOW** (do not proceed to job-cv)

## Output

### Generated files

```text
data/applications/{app_id}/
└── {app_id}-fit-report.md   # Validated fit report
```

### Confirmation message (if continuing)

```text
Fit analysis validated.

Role: {title} @ {company}
Score: {score}/100
Recommendation: {go|consider|no-go}

Main strengths:
- {strength 1}
- {strength 2}

Gaps to address:
- {gap 1}
- {gap 2}

Next step: job-cv to generate an adapted CV
```

## Notes

- The score is indicative and must be contextualized
- Talking points are suggestions to personalize
- Always verify that cited evidence is accurate
- The user can stop the workflow if the fit is too low
