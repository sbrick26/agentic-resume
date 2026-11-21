---
name: write-bullet
description: Draft one or a few resume bullets from story text the user pastes or names, following the resume rules. Use for quick drafting in chat without touching files.
---

Write the bullets the user asks for from the story text given (or the named
story files, if they exist). Rules:

1. Use only facts and numbers in the story. Never state a number the story
   lacks, not even as an example, a hypothetical, an estimate or an "if you
   know X" sample bullet. If the user asks for a figure the story does not
   have, say it is missing, ask for it, and write the bullet with the numbers
   the story does have.
2. Start with a past-tense verb; at most 25 words; one idea; outcome last.
3. Never write a client name from privacy/client-names.txt or one the user
   marks as private; use the generic description.
4. No em or en dashes. None of the words in the "Words to avoid" list of
   writing-style/STYLE.md (if present), and never: spearheaded, leveraged,
   passionate, seamlessly.
5. Output only the bullets plus, if needed, one short line naming what is
   missing.
