# ADR 0002 — Drop task-management and weekly-reports

**Status:** Accepted, 2026-05-16.
**Supersedes (partially):** [ADR 0001 §1](0001-scoping.md) — removes
`task-management` and `weekly-reports` from the in-scope list.

## Context

ADR 0001 carried over three skills from the private `cv` repo into
`inflecv`: `job-application`, `task-management`, and `weekly-reports`.
A content review against the headline claim ("decide what to put on a
CV given an offer, then journal every application") found that only
`job-application` serves that claim.

`task-management` (WSJF prioritization, `task-next` / `task-create` /
`task-start` / `task-complete` / `task-validate` / `task-archive`) and
`weekly-reports` (CFD + weekly markdown reports) are generic
internal-project-management infrastructure. Their own SKILL.md
frontmatter describes them as scaffolding for "le projet CV" — the
maintainer's private workflow, not the public toolkit.

Cost of carrying them: ~45 files (27 Python modules under
`scripts/task_management/` + `scripts/reports/`, 16 markdown files
across two skills, 2 files in `.tasks/`), dual maintenance burden, a
muddled pitch, and overlap with `daily-ops` which already handles the
maintainer's daily/weekly workflow externally.

## Decision

Remove from the repo:

- `.agents/skills/task-management/`
- `.agents/skills/weekly-reports/`
- `scripts/task_management/`
- `scripts/reports/`
- `.tasks/`
- `docs/WEEKLY_REPORTS.md`
- Related `[project.scripts]` entries (`generate-cfd`) and any
  `justfile` recipes that target the removed modules.

Update `README.md` and `AGENTS.md` to reflect the narrower scope:
inflecv ships **one** skill (`job-application`) plus the Typst CV
template, John Doe example, and supporting Python (verification only).

The removed code is not extracted to a separate repo — if it turns
out to have standalone value, recover it from git history.

## Consequences

### Positive

- Repo's pitch matches its contents: analyze → fit → adapt → journal,
  delivered via one skill + Typst + a thin verification CLI.
- Smaller surface to maintain, document, and translate (Block C).
- No ambiguity about whether contributors should extend
  task-management features.

### Negative

- ADR 0001's "Periphery / In" list is now outdated until edited.
- Anyone who cloned the repo expecting WSJF/CFD tooling loses it
  (mitigated: pre-v0.1.0, no users yet per `STATUS.md` / `CHANGELOG`).
- `pyproject.toml` test coverage / pathing needs a sweep after
  deletion.
