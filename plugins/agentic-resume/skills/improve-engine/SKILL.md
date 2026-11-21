---
name: improve-engine
description: Monthly improvement pass. Reads eval results and the user's Rework notes, finds the 3 weakest spots, and proposes fixes with before and after eval scores. Use on the first review of each month.
---

1. Collect: eval results since last month, every Rework note (each must
   already be a golden case), hard-check failures, lines the user edited.
2. Pick the 3 weakest spots. For each, propose one fix: a skill or agent
   prompt change, a STYLE.md rule, a rubric weight, a new hard check, or a
   model change.
3. Label each fix general (helps any user of the plugin: goes to the
   agentic-resume repo) or personal (only this user: goes to their repo).
4. Run the full eval suite before and after each fix. Keep only fixes that
   raise the score and break no hard check.
5. Open the PRs; never merge. Report the score changes in under 100 words.
