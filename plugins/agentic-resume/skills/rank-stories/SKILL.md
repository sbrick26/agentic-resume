---
name: rank-stories
description: Score stories with the rubric (impact, metric strength, role fit, recency, 1 to 5 each), rewrite stories/INDEX.md and show the resume set. Use when the user asks which stories are strongest or before writing the resume.
---

Run `ar-rank --json --top 8`. Report problems (missing or out of range
scores) first, then the top stories as a short table. The rubric is in
templates/stories-README.md of the plugin repo and the user's
stories/README.md. Stories marked `never_public: true` are never picked.
