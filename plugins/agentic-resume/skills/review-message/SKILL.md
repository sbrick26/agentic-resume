---
name: review-message
description: Write the one short review message for a pending review PR, ready to relay to the user wherever they read it. Use at the end of the review-pr skill.
---

Write it short and readable: under 120 words before the table, plain words.

```
Review ready: <date>
What changed: 2 to 4 bullets in plain words (resume, site, stories)
Preview: <link>      Recording: <file>
Checks: <n> pass, <n> fail | style <x>/5 | cost $<x>
Ideas to tick: up to 3, one line each
Risks: only if any, one line each
Reply Approve, or Rework with notes.
```

Never include a client name, a secret, or a story file path. Run `ar-guard`
on the message file before sending.
