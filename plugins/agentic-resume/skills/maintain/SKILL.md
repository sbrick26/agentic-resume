---
name: maintain
description: Daily health check, script first. Reports only problems. Use from a daily schedule or when the user asks if everything is healthy.
---

Check, and report only failures in under 60 words:
- the last scheduled check-in and review ran (see career-log and git log)
- `ar-check` passes on the main branch
- the inbox is empty after processing
- stories have no scores out of range (`ar-rank --no-write`)
- open questions older than 30 days (list at most 3)
- the live site returns 200 and its security headers are present (curl -sI)
