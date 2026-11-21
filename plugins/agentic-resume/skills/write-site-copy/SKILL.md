---
name: write-site-copy
description: Refresh site text (updates feed, about, project blurbs) from stories and recent career-log entries, in the user's style, with no client names. Use before a review PR or when the user asks.
---

1. Read site/ content files the user keeps (for example site/content/*.json)
   and the stories changed since the last review.
2. Delegate drafting to `resume-writer` with STYLE.md and the generic names
   from privacy/client-names.txt. Keep the site's existing structure.
3. Run `ar-guard` and `ar-lint` on the changed files; fix failures.
4. List the changes in plain words.
