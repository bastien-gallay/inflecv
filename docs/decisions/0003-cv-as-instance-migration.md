# ADR 0003 — cv-as-instance migration

**Status:** Accepted, 2026-05-18.
**Implements:** [ADR 0001 §2](0001-scoping.md) — the maintainer's
private `cv` repo becomes an *instance* of inflecv.

## Context

Inflecv was extracted from `~/Dev/personal/cv` on 2026-05-16 with no
shared git history. By 2026-05-18 the two repos held many files with
the same name and divergent content (`src/cv.typ`, `src/cv-data.typ`,
`src/shared/{config,sidebar}.typ`, `scripts/lib/__init__.py`,
`scripts/tests/test_lib.py`, `pyproject.toml`, `justfile`, `CLAUDE.md`,
`README.md`, `VERIFICATION.md`, `.gitignore`, `docs/GIT_WORKFLOW.md`),
plus several public-but-missing features that never made it upstream
during the initial extraction — notably the real implementations of
`scripts/job_analyze/` and `scripts/job_fit/`, which sat on cv feature
branches `task/INF-009-skill-analyse-offre-emploi` and
`task/INF-010-skill-analyse-adequation` as **empty stubs** in inflecv.

Two practical problems followed:

1. The headline "analyse → fit → adapt → journal" pipeline did not
   actually run from a clean inflecv clone — half the modules were stubs.
2. The maintainer's private cv kept the WSJF / weekly-reports
   scaffolding that inflecv had already dropped in
   [ADR 0002](0002-drop-task-management.md), making divergence worse
   over time.

The maintainer's stated intent (ADR 0001 §2) is that cv is an
*instance* of inflecv — same scaffolding, private content on top. The
disjoint-histories problem made this hard to express via `git merge`.

## Decision

Rebuild `~/Dev/personal/cv` as a fresh clone of inflecv with the
private layer reapplied on top, and treat history loss on `cv-bastien-gallay:main` as
acceptable provided the prior tree is preserved on a side branch.

Concretely:

1. **Phase 0 — Freeze cv-legacy on the private remote.**
   Mirror inflecv's ADR 0002 cleanup *first* (in the old cv repo), then
   commit every untracked working-tree file (brainstorms, scoping
   notes, in-flight applications), then push the whole state to a
   dedicated `archive/legacy` branch on `bastien-gallay/cv-bastien-gallay`.
   `archive/legacy` is the durable record of "what cv was the day
   before migration". Daily-ops state (`.personal/`) and caches are
   excluded via `.gitignore`.

2. **Phase 1 — Port public-but-missing modules upstream first.**
   Copy `scripts/job_analyze/` (cv branch INF-009, 12 files / 1656 LOC)
   and `scripts/job_fit/` (cv branch INF-010, 8 files / 1058 LOC) into
   inflecv. Both modules are pure stdlib, depend on none of the removed
   ADR-0002 code, and contain no personal data. Test count rises from
   154 → 296. Without this step, a fresh inflecv clone has no working
   pipeline; the migration would silently delete behaviour.

3. **Phase 2 — Rename cv → cv-legacy, clone inflecv into a fresh cv.**
   Decouple the new cv from inflecv's git history (`rm -rf .git && git
   init -b main`) so it can be force-pushed to `cv-bastien-gallay`
   without `git push --force` complaining about unrelated histories.
   Add `upstream = bastien-gallay/inflecv` immediately so future
   `git fetch upstream` works.

4. **Phase 3 — Reapply the private layer from cv-legacy.**
   Copy private content (applications, resources, brainstorms, daily-ops
   state, real Typst data + assets), overwrite the diverged shared
   files (`src/cv.typ`, `src/shared/{config,sidebar}.typ`), add the
   instance-only Typst variants (`cv-en.typ`, `cv-short.typ`,
   `cv-en-short.typ`, `src/shared/{experiences,i18n,sections,
   side-projects}.typ` — these are technically "should be upstream"
   but porting them is deferred to a later release).

5. **Phase 4 — End-to-end test in the new cv.** Install, build all
   four PDFs, run pytest, smoke-import the pipeline modules,
   confirm daily-ops still sees the repo at the unchanged path.

6. **Phase 6 — Force-push to `cv-bastien-gallay:main`.**
   `archive/legacy` (from Phase 0) protects the prior tree.
   `--force-with-lease` is intentional — we are replacing main
   wholesale by design.

## Consequences

### Positive

- The public pipeline now actually runs. `scripts/job_analyze` +
  `scripts/job_fit` are no longer empty stubs.
- `cv` and `inflecv` now share a definable relationship: cv is a fork
  whose `main` started by copying inflecv@`<sha>` and then diverged
  only on instance-specific files. `git fetch upstream && git merge
  upstream/main` will conflict only on the files in §3 of the gap
  analysis — predictable, resolvable as "ours".
- The archive branch is grep-able and link-able; nothing of the
  pre-migration cv is unrecoverable.
- The maintainer's cv repo's pre-migration `main` carried task-management
  scaffolding superseded by ADR 0002; the new `main` does not. Drift
  with the public toolkit shrinks.

### Negative

- `cv-bastien-gallay:main`'s linear history is broken. Future tooling
  that walks `git log` will see two roots: `archive/legacy` (the old
  history) and `main` (the new instance). Acceptable cost — the
  maintainer explicitly traded history preservation for a clean
  divergence model. Most historical artefacts in cv already lived as
  date-named files outside git anyway.
- The instance must override `.gitignore` to *un*-ignore `.personal/`
  and `data/applications/*` (inflecv's `.gitignore` excludes both,
  because in the public toolkit those are private; in the private
  instance, they ARE the payload). Documented inline in the new cv's
  `.gitignore`.
- Two cv branches on the GitHub remote — `task/INF-009-…` and
  `task/INF-012-skill-cv-adapte` — still exist as historical context.
  They are not referenced by `main`; safe to delete later if noisy.

## Forward note for contributors

A community contributor who asks "can I use inflecv with my own CV?"
should follow the same shape this ADR codifies:

1. Fork `bastien-gallay/inflecv` to your own GitHub org.
2. Clone your fork locally.
3. (Optionally `rm -rf .git && git init` if you want a clean history.)
4. Drop your real CV data into `src/cv-data.typ`, your real photos into
   `src/assets/`, your real `data/applications/<slug>/` bundles.
5. Override `CV_NAME` in `justfile` (or set the env var) so output PDFs
   carry your name.
6. Override `.gitignore` to un-ignore `.personal/` and
   `data/applications/*` *only if* your fork is private. Public forks
   should keep inflecv's defaults.
7. Push to your own private repo.

This shape (instance = clone + reapplied private layer) is the
contract. Inflecv is not a template engine — there is no `inflecv init`
command yet (HANDOVER.md P1). For now the "scaffolding" step is just a
git clone.

## References

- `/Users/bastiengallay/.claude/plans/zazzy-petting-widget.md` — the
  execution plan that produced this ADR.
- inflecv commits introducing the ports: `feat(job-analyze): port real
  implementation from cv INF-009`, `feat(job-fit): port real
  implementation from cv INF-010`.
- `bastien-gallay/cv-bastien-gallay:archive/legacy` — the frozen
  pre-migration tree.
