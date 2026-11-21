---
name: style-check
description: Check text against the user's writing style. Hard checks with ar-lint, then a graded style score from eval-grader. Use on any resume or site draft.
---

1. Run `ar-lint --mode professional <files>` (use `--mode casual` only for
   social posts). Any failure fails the check.
2. Delegate to `eval-grader` for the style score per item (1 to 5, with
   reasons). 4 or more on every item passes.
3. Report pass or fail, the lowest-scoring lines and why, in under 80 words.
