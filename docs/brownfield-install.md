# Brownfield install — adopting inflecv on an existing CV repo

This document inventories the conflicts an existing personal CV repo
faces when it adopts inflecv as upstream, and proposes a category-based
resolution strategy. The reference instance is the maintainer's
`~/Dev/personal/cv`. ADR 0003 codifies the one-shot migration that
produced the reference instance; this document describes the *steady
state* a contributor reaches afterwards (or directly, on a fresh fork).

## 1. Conflict inventory

Comparing a typical instance (`../cv`) against the inflecv layout
yields four categories.

### 1.1 Files that diverge in content (same path, different bytes)

| Path | Nature of conflict |
|---|---|
| `.gitignore` | instance un-ignores `.personal/` and `data/applications/*`; inflecv ignores both |
| `justfile` | instance adds multi-variant build recipes (e.g. `cv-en`, `cv-short`) + `CV_NAME` override |
| `src/cv.typ` | instance entry point — visual/structural tweaks |
| `src/cv-data.typ` | instance holds real personal data; inflecv holds the John Doe sample |
| `src/shared/config.typ` | instance-tweaked layout config |
| `src/shared/sidebar.typ` | instance-tweaked sidebar |

These are the only files where a naive `git merge upstream/main` would
conflict. Resolution policy: **prefer "ours"** — the instance owns the
visible CV; inflecv owns the scaffolding.

### 1.2 Paths only on the instance side (private payload)

These should never appear in inflecv and should stay gitignored upstream:

- `.personal/` — daily-ops state, scratch notes
- `data/applications/<slug>-<date>/` — every real job application bundle
- `dist/*.pdf` — instance build outputs
- `src/assets/*.{jpg,png}` — real photos, diplomas, logos
- `brainstorm/`, `posts/`, `resources/`, `docs/prospectives/` — instance
  research, drafts, audits, templates

### 1.3 Paths only on the instance side that arguably belong upstream

These are technically "should be upstream" but porting is deferred:

- `src/cv-en.typ`, `src/cv-short.typ`, `src/cv-en-short.typ` —
  language/length variants
- `src/shared/experiences.typ`, `i18n.typ`, `sections.typ`,
  `side-projects.typ` — shared content modules the variants depend on

Until ported, an instance that wants these variants keeps them locally.
A fresh fork that does not want them ignores this category entirely.

### 1.4 Paths only in inflecv

- `docs/decisions/000X-*.md` — ADRs (instance inherits on fetch)
- `src/assets/placeholder-photo.svg` — the John Doe placeholder; safe
  to keep on the instance or drop
- `dist/CV-John-Doe-2026-05.pdf` — sample PDF; instance discards

## 2. Resolution strategy by category

| Category | Resolution |
|---|---|
| §1.1 diverging files | instance owns; on `git merge upstream/main` resolve as "ours" |
| §1.2 private payload | gitignored on instance side via additive `.gitignore` rules; never sent upstream |
| §1.3 deferred-upstream | kept on instance until ported; no upstream conflict |
| §1.4 upstream-only | flows down on `git fetch upstream`; no resolution needed |

## 3. Brownfield install — concrete steps

For an existing personal CV repo to adopt inflecv as upstream:

1. **Add inflecv as upstream remote.**

   ```bash
   git remote add upstream https://github.com/bastien-gallay/inflecv.git
   git fetch upstream
   ```

2. **Override `.gitignore` to un-ignore the private payload.** Append
   to the instance's `.gitignore` (or to a tracked `.gitignore.instance`
   sourced from it):

   ```gitignore
   # Instance override — these ARE the payload on a private fork.
   !.personal/
   !data/applications/
   ```

   Public forks should keep inflecv's defaults and NOT un-ignore these.

3. **Decide on §1.3.** If the instance wants EN/short variants, keep
   `src/cv-en.typ` & friends. If not, delete them.

4. **Set `CV_NAME` in `justfile` (or env)** so output PDFs carry the
   instance owner's name, not "John Doe".

5. **Periodically sync from upstream.**

   ```bash
   git fetch upstream
   git merge upstream/main
   # Conflicts will be limited to the §1.1 files. Resolve as "ours".
   ```

## 4. Greenfield alternative

A contributor with no existing CV repo skips brownfield entirely:

1. Fork `bastien-gallay/inflecv` on GitHub.
2. Clone the fork locally.
3. Drop real data into `src/cv-data.typ` and `src/assets/`.
4. Set `CV_NAME` in `justfile`.
5. (Private fork only) un-ignore `.personal/` and `data/applications/`.
6. Push.

See ADR 0003 §"Forward note for contributors" for the same shape in
ADR form.

## References

- [ADR 0003 — cv-as-instance migration](decisions/0003-cv-as-instance-migration.md)
- [ADR 0001 — scoping](decisions/0001-scoping.md) §2: cv is an instance
  of inflecv
