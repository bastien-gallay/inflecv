# inflecv

> Your CV, infléchi for every opportunity. Analyze, adapt, track.

`inflecv` turns your CV from a static document into a **per-application
pipeline**. Where renderers like [typst-cv][typst-cv], [RenderCV][rendercv],
or [JsonResume][jsonresume] *render* your CV, inflecv **decides what to put
on it given a specific job offer**, then keeps a tracked journal of every
application.

**Status:** v0.1.0 — early, working, not yet released to PyPI. APIs may
break. See [`STATUS.md`](STATUS.md) for maintenance posture.

## What it does

```text
┌──────────────────┐
│  Job offer text  │
└────────┬─────────┘
         │
         ▼
   ┌───────────┐    ┌──────────────────┐
   │  analyze  │───▶│ structured offer │
   └─────┬─────┘    │ (must-haves, ATS │
         │          │  keywords, …)    │
         ▼          └──────────────────┘
   ┌───────────┐    ┌──────────────────┐
   │    fit    │───▶│ score 0-100      │
   └─────┬─────┘    │ + talking points │
         │          │ + go/no-go       │
         ▼          └──────────────────┘
   ┌───────────┐    ┌──────────────────┐
   │ adapt-cv  │───▶│ Typst CV tuned   │
   └─────┬─────┘    │ to this offer    │
         │          └──────────────────┘
         ▼
   data/applications/{company-slug-date}/
     ├── job-posting.md
     ├── analysis.md
     ├── fit-report.md
     ├── cv-adapted.typ → cv-adapted.pdf
     └── (cover-letter coming)
```

Every step is delivered as an **agent skill** (Claude / Codex / Cursor /
Aider) — markdown workflows your AI agent follows — composed with a
small Python verification CLI and the Typst template. Your agent
doesn't have to be Claude.

## Quick start

```bash
# Clone
git clone https://github.com/<you>/inflecv && cd inflecv

# Install runtime deps (Typst, uv, fonts) one-shot
./scripts/install.sh

# Build the John Doe example CV
just build

# See dist/cv.pdf
open dist/cv.pdf
```

To use your own CV, fork or template this repo, replace
`src/cv-data.typ` with your data, drop your photo into `src/assets/`.

### Bring your own CV (brownfield / greenfield)

If you already have a personal CV repo and want to adopt inflecv as
upstream, see [`docs/brownfield-install.md`](docs/brownfield-install.md).
It inventories the conflicts an existing instance faces, defines four
resolution categories (diverging files, private payload, deferred
upstream, upstream-only), and gives concrete steps to:

- add inflecv as the `upstream` remote on your repo,
- override `.gitignore` to un-ignore your private payload
  (`.personal/`, `data/applications/`) on private forks,
- sync from upstream over time (`git fetch upstream && git merge
  upstream/main`).

A fresh fork (greenfield) follows a shorter shape covered in the same
document.

## Architecture

```text
.
├── AGENTS.md              # Agent-agnostic entrypoint (Claude/Codex/Cursor/…)
├── .agents/               # Source of truth for skills
│   └── skills/            # job-application (analyze, fit, adapt-cv, letter)
├── src/                   # Typst CV sources (John Doe sample)
├── scripts/               # Python CLI: verification
├── docs/                  # Decisions, workflow, CI plan
├── data/applications/     # Per-application bundles (yours; gitignored
│                          # except the example)
└── justfile               # Build automation
```

## Audience

- **Primary:** developers using an AI coding agent (Claude Code, Codex,
  Cursor, Aider) who apply to jobs or freelance opportunities and want a
  reproducible, tracked, AI-tailored pipeline instead of ad-hoc
  copy-paste.
- **Secondary:** freelance consultants tailoring proposals per
  opportunity.

If you just want a static CV renderer, use [typst-cv][typst-cv] or
[RenderCV][rendercv] directly — `inflecv` composes with those rather
than replacing them.

## Differentiators

| Concurrence | `inflecv` |
|---|---|
| CV-centric | Application-centric |
| Static render | Dynamic pipeline per offer |
| One-shot | Journaled multi-application history |
| Template | Agent-guided workflow (agent-agnostic) |

## Status, license, governance

- **License:** MIT (see [`LICENSE`](LICENSE))
- **Code of Conduct:** [Contributor Covenant 2.1](CODE_OF_CONDUCT.md)
- **Contributing:** [`CONTRIBUTING.md`](CONTRIBUTING.md) — solo maintainer, best-effort, no SLA
- **Maintenance posture:** [`STATUS.md`](STATUS.md)
- **Coding standards:** [`CODING_STANDARDS.md`](CODING_STANDARDS.md) — Tidy First, CUPID, TDD+Reflect

## Acknowledgements

- Upstream Typst template: [neat-cv][neat-cv] by UntimelyCreation (MIT)
- Inspired by the broader CV-as-code ecosystem ([typst-cv][typst-cv],
  [RenderCV][rendercv], [JsonResume][jsonresume])

[typst-cv]: https://github.com/UntimelyCreation/typst-neat-cv
[neat-cv]: https://github.com/UntimelyCreation/typst-neat-cv
[rendercv]: https://rendercv.com/
[jsonresume]: https://jsonresume.org/
