# Contributing to inflecv

Thanks for the interest. Read this once before opening a PR.

## TL;DR posture

- **Solo maintainer**, best-effort review, **no SLA**.
- **No feature PR without an issue first.** Bugfixes, typos, doc fixes
  can go straight to PR.
- **Lazy consensus** on small PRs: one round of review, accept or
  reject. No bikeshedding.
- Quality gates are non-negotiable: tests must pass, linters must pass.
  See [`CODING_STANDARDS.md`](CODING_STANDARDS.md) for the working
  agreement (Tidy First / CUPID / TDD+Reflect / Clean Code).
- We follow [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

If life happens and the project goes quiet, see [`STATUS.md`](STATUS.md)
— it's the public-facing maintenance signal. "Maintenance mode" means
fork freely; the door doesn't have to stay propped open if it costs the
maintainer their evenings.

## What we accept

| Kind | Path |
|---|---|
| **Bug fix** | PR directly. Reference the issue if one exists. |
| **Doc fix / typo** | PR directly. |
| **Test added for existing behaviour** | PR directly (Tidy First — pin behaviour before refactor). |
| **Refactor / Tidy** | PR directly **if** it preserves behaviour. No-op diffs only. |
| **Small feature** (< 100 LoC) | Open an issue tagged `proposal` first. Wait for thumbs-up before code. |
| **Large feature** | Issue → discussion → mini-design (3 paragraphs in the issue) → PR. |
| **New skill / agent integration** | Issue describing target agent (Codex, Cursor, Aider…) + what it adds vs the Claude Code path. |
| **Breaking API change** | RFC-style issue. Justify the break, propose migration. |

## What we don't accept

- Cosmetic-only refactors without behaviour or readability gain.
- "Cleanup" PRs that mix tidying with behaviour change. Split them
  (Tidy First).
- Dependencies added for one-line convenience.
- Replacing tested code with "more idiomatic" code that lacks tests.
- Feature flags / abstractions for hypothetical future needs.

## Dev loop

```bash
# Setup
./scripts/install.sh

# Run tests
just test

# Lint
just lint

# Build CV (smoke test)
just build
```

## PR checklist

- [ ] Diff is **one of**: tidy, behaviour change, doc, dependency
  update. Not a mix.
- [ ] Tests added (for new behaviour) or updated (for changed
  behaviour).
- [ ] Linters pass: `just lint`.
- [ ] No new dependency without `## Why` in the PR description.
- [ ] Commit messages follow [GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md).
- [ ] If this affects user-facing behaviour, `CHANGELOG.md` updated
  under `## Unreleased`.

## Filing issues

A useful bug report has:

1. **What you did** — exact command line + relevant config.
2. **What you expected** — one sentence.
3. **What happened** — output / traceback. Logs > screenshots.
4. **Environment** — OS, Python version, Typst version, agent (Claude
   Code, Codex…).

A useful feature request has:

1. **The problem** in one sentence (not the solution).
2. **The user** experiencing it (P1 dev applying to jobs? P2
   freelancer? something new?).
3. **One concrete scenario** end-to-end.
4. **What you've already tried.**

## Communication

- GitHub issues for everything that has a clear question or scope.
- GitHub Discussions for "is this a good idea?" before opening an
  issue.
- No private channels, no DMs for project work.

## Maintainer biases (so you know what you're walking into)

- I optimise for *not adding code* before adding code.
- I'll push back on abstractions before there are three concrete uses.
- I prefer small, frequent releases to long-running branches.
- I'd rather close a stale issue than leave it lingering.
