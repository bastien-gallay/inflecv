# CV Verification Checklist

Systematic guide for checking CV quality before sending it out.

## Usage

Before each final CV export, walk through this checklist and tick each
verified item. For automated checks, run: `just validate`.

---

## 1. Compilation

- [ ] The CV compiles without error (`just build`)
- [ ] The PDF is generated in `dist/cv.pdf`
- [ ] The PDF opens correctly in a PDF reader
- [ ] Text is selectable (not a rasterized image)
- [ ] Links are clickable in the PDF

## 2. Contact information

- [ ] Full name is correct
- [ ] Professional email is valid and up to date
- [ ] Current phone number (international format)
- [ ] Address / location is consistent
- [ ] LinkedIn link works
- [ ] GitHub link works (if present)
- [ ] Other links verified (portfolio, personal site)

## 3. Spelling and grammar

- [ ] Job title is correct
- [ ] Company names are spelled correctly
- [ ] Technology names are spelled correctly (e.g. TypeScript, PostgreSQL)
- [ ] No spelling mistakes in descriptions
- [ ] Diacritics are correct (for non-English text)
- [ ] Capitalization is appropriate (sentence starts, proper nouns)

## 4. Date consistency

- [ ] Uniform date format throughout the CV
- [ ] Dates in reverse chronological order (most recent first)
- [ ] No inconsistent date overlaps
- [ ] Start and end dates are consistent for each role
- [ ] Correct current year for ongoing roles ("Present" or current year)

## 5. Style consistency

- [ ] Uniform verb tense (present or past, not mixed)
- [ ] Consistent writing style (bullet points vs paragraphs)
- [ ] Similar level of detail for comparable roles
- [ ] Consistent use of abbreviations
- [ ] Uniform punctuation (trailing periods on bullets, commas)

## 6. Visual formatting

- [ ] Sections are correctly aligned
- [ ] Uniform spacing between sections
- [ ] Readable font at an appropriate size
- [ ] No text cut off or overflowing
- [ ] Sidebar sized correctly (no overflow)
- [ ] Page breaks land in the right places
- [ ] No orphaned sections (title alone at the bottom of a page)

## 7. Professional content

- [ ] "About" section is concise and impactful
- [ ] Skills are relevant to the target role
- [ ] Experience descriptions focus on results / impact
- [ ] Certifications include validity dates
- [ ] Education lists degrees obtained
- [ ] No outdated or irrelevant information

## 8. Privacy and security

- [ ] No sensitive information (national ID number, exact birth date)
- [ ] No confidential information from previous employers
- [ ] No mention of NDA-covered projects without permission
- [ ] No financial information (salaries, revenue figures)

## 9. Length and readability

- [ ] Appropriate length for the profile (junior: 1 page, senior: 2 pages)
- [ ] Key information visible in under 30 seconds (scanning test)
- [ ] Priority sections at the top of the CV
- [ ] No areas that are too dense or too empty

## 10. Final check

- [ ] Full read-through out loud
- [ ] Mobile screen display test
- [ ] Print test (or print preview)
- [ ] Third-party review if possible
- [ ] Filename appropriate for sending

---

## Automated verification scripts

```bash
# Run all checks
just verify

# Individual checks
just verify-build   # Compilation
just verify-dates   # Date consistency
just verify-format  # Basic formatting

# Run the verification test suite
just test-verify
```

## Verification frequency

| Situation | Verification level |
|-----------|--------------------|
| Minor change (typo) | Compilation only |
| Adding or modifying content | Compilation + affected sections |
| New application | Full checklist |
| Major update | Full checklist + third-party review |

---

## Common issues

| Issue | Resolution |
|-------|------------|
| PDF not generated | Check Typst syntax, rerun `just build` |
| Text overflows the sidebar | Reduce content or increase `sidebar-width` |
| Inconsistent dates | Check chronological order and format |
| Broken links | Update URLs in `cv.typ` |
| Missing fonts | Check that system fonts are installed |

---

Last updated: 2026-05-16.
