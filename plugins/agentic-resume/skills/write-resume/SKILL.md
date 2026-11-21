---
name: write-resume
description: Write or update the resume from the top stories, in the user's writing style, with every claim traced and no client names. Use when the user asks for a resume draft or a review PR needs one.
---

1. Run `ar-rank --json --top 8` to choose stories.
2. Delegate to the `resume-writer` agent with: the chosen story files,
   writing-style/STYLE.md, profile/profile.md, privacy/client-names.txt.
3. Run `ar-check`. If anything fails, send the failures back to
   resume-writer, at most 2 rounds, then stop and report.
4. Run the style-check skill on resume/resume.md.
5. Report in under 100 words: what changed, the style score, open questions.
