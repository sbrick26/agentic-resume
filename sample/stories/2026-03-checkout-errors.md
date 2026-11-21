---
title: "Cut checkout errors for a regional freight company"
period: 2026-03
status: past
client: "a regional freight company"
scores:
  impact: 5
  metric_strength: 5
  role_fit: 5
  recency: 5
  total: 20
metrics:
  - value: "4.1 to 0.6"
    unit: "percent of checkouts failing"
    basis: direct
    how_estimated: "error dashboard, 30 days before and after"
sources: ["sample"]
public_ok: true
never_public: false
open_questions: []
---

## Situation
Shippers abandoned bookings because checkout failed about one time in 25.

## What I did
Traced the failures to a retry storm in the payment step, added idempotency keys and a circuit breaker, and wrote the runbook.

## Outcome
Checkout errors fell from 4.1 to 0.6 percent in 30 days, and the team adopted the runbook for every payment change.
