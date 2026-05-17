# Coding Standards

This file is the working agreement for code in this repo. It is meant
to be re-read on a slow day, not skimmed once. Four pillars, in the
order you usually apply them:

1. **Tidy First** — separate behaviour changes from clean-ups.
2. **CUPID** — properties to aim for in design and refactoring.
3. **TDD (Red → Green → Refactor → Reflect)** — the loop that keeps the
   above honest.
4. **Clean Code** — local taste rules that survive automation.

Repo-specific rules in [`AGENTS.md`](AGENTS.md) take precedence when
they collide.

---

## 1. Tidy First (Kent Beck)

> *Make the change easy, then make the easy change.*

Behaviour changes and structural changes are **two different commits**.

- **Tidying** — renames, extractions, dead-code removal, reformatting,
  splitting a long function, adding a missing test that pins existing
  behaviour. Never alters observable output.
- **Behaviour change** — the actual feature, fix, or contract change.

Rules of thumb:

- If the diff to add a feature feels too big, stop. Tidy the surrounding
  code first (in its own commit), then come back. The feature commit
  shrinks.
- Tests that pin existing behaviour are **Must-have**, not Could-have.
  Land them *before* the behaviour change.
- If a tidy ends up changing observable behaviour, it wasn't a tidy.
  Revert and split.

Acceptable commit shapes:

```text
✅  refactor(job-fit): extract _score_dimension helper        (tidy)
    feat(job-fit): weight dimensions per config               (behaviour)

❌  feat(job-fit): weight dimensions per config + cleanup
```

---

## 2. CUPID (Dan North)

Five properties to optimise for, in roughly this order:

| Property | One-liner | Smell when violated |
|---|---|---|
| **Composable** | Plays well with others; small surface, no surprises. | "I have to mock half the world to test this." |
| **Unix philosophy** | Does one thing well. | Module/class with `and` in its purpose statement. |
| **Predictable** | Behaves as expected; no hidden state. | "Works on my machine" / order-dependent tests. |
| **Idiomatic** | Reads like the language and the codebase. | Reviewer says "this is clever" with a sigh. |
| **Domain-based** | Names match the user's vocabulary. | Generic `Manager`/`Helper`/`Util` names. |

In this repo specifically:

- **Composable** — Each script (`job_analyze`, `job_fit`, `verification`)
  is callable standalone via CLI. They emit JSON. Don't reach into
  another module's internals.
- **Unix** — One CLI per concern. Pipe-friendly is the goal.
- **Predictable** — Same inputs → same outputs. Tests must be
  deterministic.
- **Idiomatic** — Typer for CLI, dataclasses for state, `pathlib` over
  `os.path`, `pytest` over `unittest`. Match what's already there.
- **Domain-based** — `JobPosting`, `FitReport`, `Application`,
  `CVAdaptation`. Not `Container`, `Manager`, `Item`.

---

## 3. TDD with a fourth step — Reflect

The standard Red → Green → Refactor loop, with a deliberate **Reflect**
beat at the end of each cycle.

```text
   ┌──────────┐
   │   RED    │   Write the smallest failing test that names the
   │          │   behaviour you want.
   └────┬─────┘
        ▼
   ┌──────────┐
   │  GREEN   │   Write the least code that makes it pass. Ugly OK.
   └────┬─────┘
        ▼
   ┌──────────┐
   │ REFACTOR │   Clean up — names, duplication. Tests stay green.
   └────┬─────┘
        ▼
   ┌──────────┐
   │ REFLECT  │   Did this cycle make the design clearer? If not,
   │          │   stop and rethink before the next Red.
   └──────────┘
```

The **Reflect** step is what keeps the loop from grinding out lots of
small green tests that don't add up to a coherent design. Ask:

- *Is the next test going to teach me something, or am I just adding
  coverage?*
- *Does the production code now make less sense than before?*
- *Did I just introduce an abstraction with one user?*

If any answer is "yes", pause before continuing.

---

## 4. Clean Code (local taste)

Rules that survive automation. Linters do not catch these — review
does.

- **No comments that restate the code.** Comments explain *why*, not
  *what*. If the *what* isn't obvious, rename or extract.
- **No dead code.** If it's commented out, delete it. Git remembers.
- **No defensive code without a reason.** Don't validate internal
  invariants; trust your callers. Validate at system boundaries (user
  input, external APIs) only.
- **Functions do one thing.** If the docstring uses "and", split.
- **No mutable default arguments in Python.** `def f(x=[]):` is a bug.
- **No premature abstraction.** Wait for three concrete uses before
  extracting a helper.
- **Errors are values where possible.** Exceptions for exceptional
  cases, not for control flow.

---

## Style anchors (mechanical)

- Python: `ruff` for lint+format. Line length 100. Type hints
  encouraged but not enforced in tests.
- Markdown: `markdownlint` (config in `.markdownlint.json`).
- Typst: follow upstream `neat-cv` conventions; 2-space indent.
- Commits: see [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md).

When in doubt, match what the surrounding code does.
