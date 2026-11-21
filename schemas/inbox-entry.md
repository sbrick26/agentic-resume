# career-log/inbox

Every update lands here as one file before processing .
Not built yet; this documents the format.

File name: `YYYY-MM-DDTHHMM-<source>-<short-slug>.md`

```
---
date: 2026-11-21T16:05
source: duet          # chat | duet | slack | email | cli | notion | other
kind: checkin         # checkin | win | note | correction
author: owner
refs: []              # optional links: PR, doc, ticket
---
Free text in the owner's words. Numbers as they said them.
```

Add one with `ar-add-entry --source cli --kind win "text"`. Any
source adapter calls that command; nothing else writes here. Entries are
append-only; a correction is a new entry with `kind: correction`.
