# John Doe — example application bundle

This folder is the **only sample application** committed to the public
repo. Everything under `data/applications/` is otherwise gitignored.

It demonstrates the full inflecv pipeline output for one job
application. All names, companies, and details are fictional.

## Files

| File | Step | Purpose |
|---|---|---|
| `job-posting.md` | input | The offer, captured verbatim. |
| `analysis.md` | `inflecv analyze` | Structured extraction: requirements, ATS keywords, application instructions. |
| `fit-report.md` | `inflecv fit` | Score 0-100, strengths, gaps, talking points, go/no-go. |
| `cv-adapted.typ` | `inflecv adapt-cv` | Typst source tailored to this offer. (TBD) |
| `cv-adapted.pdf` | build | Compiled output. (TBD) |
| `cover-letter.md` | `inflecv cover` | Cover letter / incident narrative. (TBD — feature P1) |

## Use this as a reference

When you fork inflecv to create your own instance, study this folder
to understand what each pipeline step produces. The `analysis.md` and
`fit-report.md` formats are stable contracts — adapt your own CV
sources to fit through these passes.
