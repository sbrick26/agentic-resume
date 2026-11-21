---
name: review-pr
description: Bundle resume and site changes since the last review into one branch and pull request, with preview, checks, evals and the review message. Use on the scheduled review days or when the user asks for a review.
---

1. Create branch `review/<YYYY-MM-DD>` from main. If nothing changed in
   stories/, career-log/ or the site since the last review, stop and say
   "nothing to review".
2. Run process-inbox, then write-resume, then write-site-copy, then
   improve-site (audit and ideas; build only items the user ticked).
3. Run `ar-check` and the eval suite (`evals-harness/run.py` in the plugin
   repo, plus the user's evals/golden if present). Record pass or fail,
   style score and cost.
4. Commit. The plugin hook re-runs the checks; a failure blocks the commit.
5. Open the PR (gh pr create) with the review message as its body. Never
   merge: merging needs the user's explicit Approve.
6. Run review-message and return it.
