---
name: write-resume
description: Write or update the resume from the top stories, in the user's writing style, with every claim traced and no client names. Use when the user asks for a resume draft or a review PR needs one.
---

1. Run `ar-rank --json --top 8` to choose stories.
2. Delegate to the `resume-writer` agent with: the chosen story files,
   writing-style/ (STYLE.md and any other guide), profile/profile.md,
   profile/directives.md if present, privacy/client-names.txt.
3. Run `ar-check`. If anything fails, send the failures back to
   resume-writer, at most 2 rounds, then stop and report.
3b. Run `ar-fit`. If it does not fit one page at 10pt, send its report
   (lines over, orphan lines, long lines) back to resume-writer with the
   cut order in writing-style/RESUME-PATTERNS.md ("Fitting one page"), at
   most 2 rounds. Never cut a number or result without listing it as an open
   question for the owner. `ar-fit --pdf resume/resume.pdf` writes the page.
4. Run the style-check skill on resume/resume.md.
5. Report in under 100 words: what changed, the style score, the page fit
   (size and lines spare), open questions.
