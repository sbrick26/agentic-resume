---
title: "Moved a health tech startup to one-click deploys"
period: 2025-04
status: past
client: "a health tech startup"
scores:
  impact: 4
  metric_strength: 4
  role_fit: 5
  recency: 4
  total: 17
metrics:
  - value: "45 to 8"
    unit: "minutes per production deploy"
    basis: direct
    how_estimated: "CI timing logs"
sources: ["sample"]
public_ok: true
never_public: false
open_questions: []
---

## Situation
Deploys were manual, took about 45 minutes, and happened once a week.

## What I did
Built a CI pipeline with preview environments and a single approve-to-deploy step.

## Outcome
Deploys dropped from 45 to 8 minutes and went from weekly to daily.
