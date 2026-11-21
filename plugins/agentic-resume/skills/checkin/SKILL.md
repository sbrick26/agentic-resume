---
name: checkin
description: Daily check-in. Ask the user what they worked on today, record the answer as an inbox entry, then process it and show what changed in plain words. Use when the user says check in, logs their day, or a scheduled check-in fires.
---

1. Ask one question: "What did you work on today? Anything with a number?"
   If the user already gave their update in this message, skip asking.
2. Record their answer verbatim with
   `ar-add-entry --source chat --kind checkin "<their words>"`.
   For a win or a correction use `--kind win` or
   `--kind correction --corrects <entry file>`.
3. Ask at most two follow-ups, only for a missing number or outcome. Record
   each answer as its own entry. Never guess a number.
4. Run the process-inbox skill.
5. Reply in under 80 words: new stories, changed stories, open questions.
   The user can answer "fix: ..." to correct something (a correction entry).
