---
name: improve-site
description: Audit the user's site and propose up to 3 improvements; fix small problems directly and build only the bigger ideas the user ticked. Use during a review PR or when the user asks.
---

1. Delegate to `qa` for the live site (or preview) at desktop and 390px.
2. Delegate to `site-designer` with the qa findings for up to 3 ideas; add
   them to site/BACKLOG.md as unticked items.
3. Fix small findings directly (broken links, typos, stale dates).
4. Build only items ticked `- [x]` in site/BACKLOG.md, at most 2 per run,
   following site/design-system.md, with tests. A build that fails its
   tests 3 times goes back to the backlog with the reason.
