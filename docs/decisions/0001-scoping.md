# ADR 0001 — Scoping & first principles

**Status:** Accepted, 2026-05-13.
**Decision drivers:** create a useful OSS toolkit out of a personal
CV-as-code workflow, without leaking personal data, without locking
into one AI-agent runtime, and without making the maintainer's life
miserable.

## Context

`inflecv` is extracted from a private repo (`cv`) that combined a
Typst CV template, AI-assisted analysis/fit/adaptation skills, and the
maintainer's personal application data. The public toolkit needs to
generalise the *workflow* (analyze → fit → adapt → track) without the
personal corpus.

## Decisions

### 1. Periphery

- **In:** Typst CV template, `job-application` skill, Python
  verification CLI, installer, John Doe example.
- ~~**In:** `task-management` and `weekly-reports` skills, reporting
  Python scripts.~~ *Superseded by [ADR 0002](0002-drop-task-management.md)
  (2026-05-16): scope reduced to the job-application pipeline.*
- **Out:** all personal data — applications, audits, analyses,
  profile, daily files, photo. Stays in the maintainer's private
  fork.

### 2. Two-repo split

The OSS repo (`inflecv`) is the public source. The maintainer's
private repo becomes an *instance* — a fork that adds private data
under gitignored paths, pulls upstream changes from the OSS repo via
git remote. No reverse leak.

### 3. Positioning

`inflecv` is **application-centric**, not CV-centric.

> Where typst-cv / RenderCV / JsonResume render, inflecv decides what
> to put on the CV given an offer, then journals every application.

Composes with existing CV renderers — does not replace them.

### 4. Target audience

- **Primary (P1):** developers using an AI coding agent (Claude
  Code, Codex, Cursor, Aider) who apply to jobs or freelance
  opportunities.
- **Secondary (P2):** freelance consultants tailoring proposals.

### 5. License

**MIT**, applied uniformly to code, templates, and content. Pattern
consistent with comparable OSS perso projects (JsonResume,
typst-cv). No Apache 2.0 (overhead, headers) ; no GPL (breaks
fork-and-customize) ; no dual-licensing with CC-BY (complexity ≫
benefit at our scale).

### 6. Governance

Solo maintainer, open contributions, best-effort, no SLA. Lazy
consensus on small PRs. No CLA, no DCO, no RFC process. Contributor
Covenant 2.1 as Code of Conduct. `STATUS.md` is the canonical
maintenance signal — supports pivot to `maintenance` posture without
public drama.

### 7. Architecture: agent-agnostic

`AGENTS.md` + `.agents/` directory is the source of truth. Aliases
(symlinks or wrapper files) expose them as `CLAUDE.md` + `.claude/`
for Claude Code users. Codex, Cursor, Aider, etc. read `AGENTS.md`
directly. **No agent runtime is hardcoded.**

### 8. Self-bootstrapping installer

A `./scripts/install.sh` script installs Typst, `uv`, `just`, Python
deps, and fonts. Target: clone → install → `just build` in 3
commands on a fresh machine.

### 9. Naming

The project is named **`inflecv`** — a letter-substitution on
"inflect" (linguistic inflection = variation of a root form to fit
context). The `cv` is encoded by the final `v`. Pronounced
"in-flec-v" (EN) or "in-flèkve" (FR, near *infléchir*).

Plan B (if PyPI/NPM/domain collision discovered post-decision):
`refracv` (validated clean in pivot brainstorm). Names already burned:
`applyflow` (Sydney ATS SaaS), `cvbench` (computer-vision benchmark
namespace), `palimpsest` (phonetic), `burnish` (phonetic).

## Consequences

- The cv repo (private instance) must be reconfigured as a fork of
  inflecv with personal data under gitignored paths.
- Future skills/scripts default to `.agents/` source; aliases follow.
- Any agent-runtime-specific assumption is a regression — gate on PR
  review.
- The maintainer reserves the right to flip `STATUS.md` to
  `maintenance` if review backlog exceeds capacity. This is not an
  exit; it's a feature.

## References

- Brainstorm logs (private cv repo): naming session #1 → `applyflow`
  (burned), naming session #2 → `inflecv` (accepted).
- Mapping public/private: maintained in the private cv repo, not
  published.
