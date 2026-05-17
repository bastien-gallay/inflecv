# Handover — inflecv extraction

**Created:** 2026-05-13
**Status:** Steps 1–3b complete. Ready for Step 4 (`git init` + first
commit). **No git history yet** — this repo is not yet a git repo.
**Origin:** extracted from private `~/Dev/personal/cv/` (CV repo);
that repo retains a memory and brainstorm logs covering the decision
trail.

Read this file first when starting a new session in this repo.

## What inflecv is

OSS toolkit that turns a static CV into a per-application pipeline:
analyze job offers, score fit, adapt the CV per offer, journal every
application. Agent-agnostic (Claude Code / Codex / Cursor / Aider /
Continue).

**Positioning headline:**
> Where typst-cv / RenderCV / JsonResume render, inflecv decides what
> to put on the CV given an offer, then journals every application.

## Decisions baked in (do not relitigate without strong reason)

| Topic | Decision | Source |
|---|---|---|
| **Name** | `inflecv` (letter-sub on "inflect"; encodes `cv` via final `v`). Plan B: `refracv`. | `docs/decisions/0001-scoping.md` § 9 |
| **License** | MIT everywhere, code + content. Apache 2.0 / GPL / dual-CC-BY rejected. | `docs/decisions/0001-scoping.md` § 5 |
| **Repo model** | OSS = source. Maintainer's private CV repo becomes an *instance* (fork with gitignored personal data). | § 2 |
| **Positioning** | Application-centric pipeline, not CV renderer. Composes with existing renderers. | § 3 |
| **Audience** | P1: devs using AI coding agents who apply to jobs. P2: freelancers tailoring proposals. P3 (coachs) deferred. | § 4 |
| **Governance** | Solo maintainer + open contributions, no SLA. CoC = Contributor Covenant 2.1. No CLA/DCO/RFC. | § 6 + `CONTRIBUTING.md` |
| **Agent runtime** | Agent-agnostic. `AGENTS.md` + `.agents/` source of truth. `CLAUDE.md` + `.claude/` are aliases. | § 7 + `AGENTS.md` |
| **Installer** | Self-bootstrapping `./scripts/install.sh` (Typst, uv, just, fonts). | § 8 + `scripts/install.sh` |
| **Maintenance signal** | `STATUS.md` is canonical. Active → slow → maintenance → archived. | `STATUS.md` |
| **Coding standards** | Tidy First / CUPID / TDD+Reflect / Clean Code. | `CODING_STANDARDS.md` |

## Names burned (do not revisit)

`applyflow` (Sydney ATS SaaS collision), `cvbench` (computer-vision
benchmark namespace), `prismcv` (frontal collision with PrismCV /
PrismaCV), `refine` (saturated AI-resume), `motif` seul (X11 window
manager / Canva), `palimpsest` (phonetic in EN: "pale incest"),
`burnish` (phonetic in FR: "burne-ish"), `lapidary` (FR
connotation "rien à ajouter" friction with cover letters).

## What's in this repo (as of 2026-05-13)

- Root metadata: `README.md`, `LICENSE`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `CODING_STANDARDS.md`, `STATUS.md`,
  `CHANGELOG.md`, `AGENTS.md` (+ `CLAUDE.md` symlink),
  `pyproject.toml`, `.gitignore`, `.markdownlint.json`.
- **Skills:** `.agents/skills/job-application/` with Claude Code compat
  via `.claude/skills` symlink.
- **CV sample (John Doe):** `src/cv.typ` (data-driven, minimal) +
  `src/cv-data.typ` (schema stable) + `src/shared/{config,sidebar}.typ` +
  `src/assets/placeholder-photo.svg`.
- **Python scripts:** `scripts/{lib,verification}/` + tests +
  `scripts/install.sh`.
- **Sample application:** `data/applications/john-doe-example/`
  (job-posting + analysis + fit-report).
- **CI minimal P0:** `.github/workflows/ci.yml` (install + tests +
  tidy-first commit-shape check).
- **Docs:** `docs/decisions/{0001-scoping,0002-drop-task-management}.md`,
  `docs/GIT_WORKFLOW.md`.

## What's NOT in this repo yet

- Short / EN / EN-short CV variants. Deleted (broken imports). P1.
- `cv adapt-cv` Python CLI implementation. The Typst template
  (`.agents/skills/job-application/templates/cv-adapted-template.typ`)
  exists; the orchestration that fills its placeholders is the next
  feature. P1.
- Cover letter generator. P1+.
- Multi-language (FR/EN) sidebar via `i18n.typ`. Not extracted from
  the source repo (depended on private content). P1.
- A real photo. `placeholder-photo.svg` is a silhouette. Replace at
  your discretion.
- `uv.lock`. Deleted (was stale, referenced `neat-cv`). Regenerate
  via `./scripts/install.sh` or `uv sync`.

## Critical pre-Step-4 smoke tests

Run these from the repo root **before** the first git commit:

```bash
# 1. Install deps (regenerates uv.lock)
./scripts/install.sh

# 2. Verify tests pass
uv run pytest -q

# 3. Verify Typst builds (John Doe sample)
just build
open dist/CV-John-Doe-*.pdf
```

Likely failure points (anticipate):

- `just build` may fail if `cv.typ` data-driven layout has a field
  mismatch with what `neat-cv-local.typ` expects. The original `cv.typ`
  used many fields from `cv-data.typ` that may not all be wired up in
  the minimal rewrite. Fix by either:
  - Extending `cv.typ` to handle missing fields gracefully (preferred,
    P0 if it fails)
  - Adding the missing wiring in `shared/config.typ`
- `uv sync` may need network access for first-time install.
- `markdownlint` is optional (justfile skips if absent).

## Step 4 + Step 5 plan

```bash
cd ~/Dev/personal/inflecv

# Step 4: git init + first commit (no history from cv repo)
git init -b main
git add -A
git commit -m "feat: initial OSS extraction (v0.1.0 — John Doe sample)"

# Step 5: push to GitHub
gh repo create inflecv --public --source=. --remote=origin
git push -u origin main

# Optional: tag v0.1.0 once smoke tests green
git tag -a v0.1.0 -m "First public release"
git push origin v0.1.0
```

**Naming on GitHub:** the `pyproject.toml` URL assumes
`github.com/bastiengallay/inflecv`. Adjust if the org differs.

## Roadmap (post v0.1)

### P0 (must, before v0.1 is honestly usable)

- [ ] Validate `just build` works on a fresh machine via the installer.
- [ ] CI: green on `main` (install + tests + tidy-first check).
- [ ] Ship a working `cv adapt-cv` end-to-end demo: take John Doe
      `cv-data.typ` + the sample job posting → produce
      `data/applications/john-doe-example/cv-adapted.pdf`.
- [ ] Replace the photo placeholder if desired (Pexels portrait or
      generated). User mentioned two Pexels candidates in chat.

### P1 (post-release)

- [ ] Short CV variant (`cv-short.typ`) with data-driven layout.
- [ ] EN / FR i18n via `shared/i18n.typ`.
- [ ] Cover letter generator (`inflecv letter`).
- [ ] CI expanded: markdownlint, ruff CI strict, Typst build.
- [ ] Documentation site (mdBook or similar).
- [ ] Cookiecutter / template-repo workflow for first-time forkers.

### P2 (later)

- [ ] CI full-featured: matrix on Python versions + OS, mutation
      testing (`mutmut` already in dev deps).
- [ ] Plugin discovery for additional skills.
- [ ] Sample integrations for Codex, Cursor, Aider (currently
      Claude-Code-leaning despite agent-agnostic architecture).

## Reference brainstorm + naming decisions

The full naming session logs live in the **private cv repo** at
`~/Dev/personal/cv/brainstorm/` :

- `20260513-naming-toolkit-oss.md` — session #1, picked then dropped
  `applyflow`.
- `20260513-naming-pivot-inflecv.md` — session #2 pivot, picked
  `inflecv`. Includes the letter-sub `t→v` pattern discovery.

The `docs/decisions/0001-scoping.md` in this repo is the public
ADR-style synthesis.

## Open questions for a future session

1. **Pin `neat-cv` Typst package version** in `manifest.yml`? Currently
   imports `@preview/neat-cv:0.4.0` — pin or follow latest?
2. **CHANGELOG entries before v0.1**: should the `## Unreleased`
   section list every internal file added, or only user-visible
   features? Convention is "user-visible" — current entries are too
   granular.
3. **`STATUS.md` posture for v0.1**: ship as `active` or `slow`? Solo
   maintainer + side-project nature suggests `slow`.
4. **GitHub org name**: `bastiengallay` (personal) or a dedicated org
   (`inflecv-tools` etc.)? `pyproject.toml` assumes personal.
5. **Pexels photo licensing**: if used, attribution where? Decided
   against in the first pass — SVG silhouette ships instead.

## End-state assertion

After the smoke tests and Step 4, this repo should be:

- Buildable from a fresh clone with one command (`./scripts/install.sh`).
- Producing a valid John Doe sample PDF (`just build`).
- CI-green on `main`.
- No personal data of the maintainer outside intentional attribution
  (`LICENSE` copyright, `pyproject.toml` author).
- Forkable for a third party to use as an `inflecv` instance for their
  own CV.
