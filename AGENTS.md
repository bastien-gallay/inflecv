# AGENTS.md

Entry point for any AI coding agent operating on this repo —
Claude Code, Codex, Cursor, Aider, Continue, or anything else that
respects the [`AGENTS.md`][spec] convention.

[spec]: https://agentsmd.dev/

Repo-specific instructions live here. Agent-specific aliases (e.g.
`CLAUDE.md` symlinking to this file) keep the source of truth single.

## Project Overview

`inflecv` is an OSS toolkit that turns a static CV (Typst source) into
a **per-application pipeline**: analyze a job offer, score the fit,
adapt the CV to the offer, keep a tracked journal of every
application. Optionally generates cover letters.

The headline claim:

> Where typst-cv / RenderCV / JsonResume render, inflecv **decides what
> to put on the CV given an offer**, then journals every application.

## Repo Layout

```text
.
├── AGENTS.md            # this file — agent entry point
├── README.md            # human entry point
├── CODING_STANDARDS.md  # Tidy First / CUPID / TDD+Reflect / Clean Code
├── CONTRIBUTING.md      # solo maintainer posture
├── STATUS.md            # current maintenance posture (active/slow/…)
├── LICENSE              # MIT
│
├── .agents/             # source of truth for skills
│   └── skills/          # job-application
│
├── src/                 # Typst CV sources (John Doe sample)
├── scripts/             # Python CLIs (verification) and library code
├── docs/                # GIT_WORKFLOW, decisions/
└── data/applications/   # per-application bundles (gitignored except example)
```

## How agents should work in this repo

1. **Before doing anything**: read this file, `CODING_STANDARDS.md`,
   and `STATUS.md`. They take precedence over agent defaults.
2. **Tidy First**: never mix behaviour change with refactor in one
   commit. Split.
3. **Test before behaviour change**: pin existing behaviour with a
   test, *then* change the behaviour, in two separate commits.
4. **One CLI per concern**: don't grow `scripts/foo/__init__.py` into
   a kitchen sink. Add a new module instead.
5. **JSON out, JSON in**: any new CLI subcommand emits structured JSON
   on `--json`. Don't pretty-print as the only output.
6. **Don't reach into other modules' internals**: compose via CLI
   subprocess or via the package's public API. No `from
   .._internal_thing import _foo`.

## Naming conventions

Domain terms (use these literally in code, docs, commit messages):

- **Application** — one job application: a folder under
  `data/applications/{company-slug}-{YYYY-MM-DD}/`.
- **Job posting** — the raw offer text, saved as
  `{slug}-job-posting.md`.
- **Analysis** — structured extraction of the offer (must-haves, ATS
  keywords, …).
- **Fit report** — score + strengths + gaps + go/no-go.
- **CV adaptation** — the Typst source tailored to one application.
- **Skill** — a Markdown file under `.agents/skills/<name>/` describing
  a multi-step workflow an agent can follow. Agent-agnostic format.

Avoid: `Manager`, `Helper`, `Util`, `Service`. Names should come from
the domain.

## Build and test

```bash
./scripts/install.sh   # install Typst, uv, fonts (one-shot)
just build             # compile CV (smoke test)
just test              # run pytest
just lint              # ruff + markdownlint
just verify            # all of the above + extra QA
```

## How commits are framed

See [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md). Two-line shape:

```text
<type>(<scope>): <subject>           # 1 line, <72 chars

<body explaining why, not what>      # optional, wrapped at 72
```

Types: `feat`, `fix`, `refactor`, `tidy`, `docs`, `test`, `chore`.

## Agent-specific notes

- **Claude Code:** `CLAUDE.md` is a symlink to this file. Skills
  under `.claude/skills/` mirror `.agents/skills/`.
- **Codex / OpenAI agents:** read this file directly.
- **Cursor:** `.cursorrules` references this file.
- **Aider:** point `--read AGENTS.md` at it on startup.

If you add support for another agent runtime, add an alias entry here
and explain how it discovers this file.

## When stuck

- Read `STATUS.md` to know what maintenance pace to expect.
- Open a GitHub issue with the section heading "I'm stuck on
  X" and one concrete reproducer.
- Don't ping the maintainer outside GitHub.
