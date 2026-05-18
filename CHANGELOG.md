# Changelog

All notable changes to `inflecv` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Initial extraction from private CV repo, sanitised for OSS release.
- MIT LICENSE.
- README, AGENTS.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, STATUS.md.
- `CODING_STANDARDS.md` (Tidy First / CUPID / TDD+Reflect / Clean Code).
- `scripts/install.sh` one-shot installer (Typst, uv, just, Python deps, fonts).
- CI minimal: install + tests + tidy-first commit-shape check.
- John Doe example application bundle (sample CV + sample offer + sample fit report).
- `scripts/job_analyze/` real implementation (was an empty stub):
  parses a job posting, extracts must-haves / nice-to-haves / ATS
  keywords / red flags, emits a Markdown analysis. 80+ unit tests.
- `scripts/job_fit/` real implementation (was an empty stub):
  scores fit on the 60/20/15/5 must-have / nice-to-have / experience
  / culture formula, emits a Markdown fit report. 60+ unit tests.

### Changed

- Translated `VERIFICATION.md` and the `job-application` skill
  (SKILL + 3 workflows) to English.

### Removed

- `task-management` and `weekly-reports` skills and their Python
  scaffolding (`scripts/task_management/`, `scripts/reports/`,
  `scripts/update_priority_scores.py`, `scripts/lib/wsjf.py`,
  `.tasks/`, `docs/WEEKLY_REPORTS.md`, `resources/templates/`,
  `config/task_management/`). Rationale in
  [ADR 0002](docs/decisions/0002-drop-task-management.md): out of
  scope for the headline job-application pipeline.
