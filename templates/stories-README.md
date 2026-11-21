# stories

One Markdown file per career story. A story is one piece of work with an
outcome: a build, a deal, a deployment, a talk. Facts from the old career
hub and from check-ins roll up into stories; resume bullets and site copy are
written from stories only.

File name: `YYYY-MM-short-slug.md` (month the story started).
Start from `_template.md`.

## Rubric (each 1 to 5, total out of 20)

| Score | Impact | Metric strength | Role fit | Recency |
|---|---|---|---|---|
| 5 | Adopted or bought by a customer, or changed how a team works | Direct, measured number with a stated source | Core to the target role | Within 6 months |
| 4 | Deployed or in trial with real users | Direct number, source informal | Strong adjacent skill | 6 to 12 months |
| 3 | Won a competitive evaluation or produced pipeline | Estimate with a stated method | Useful supporting skill | 1 to 2 years |
| 2 | Measured technical result only | Estimate, method vague | Generic engineering | 2 to 4 years |
| 1 | Built, no outcome yet | No number | Off target | Older than 4 years |

Rank by total, break ties by impact. Resume takes the top stories that fit one
page; the site can show more.

## Merging duplicates

Two files describe the same story when they share the same work, the same
period and the same outcome, even if worded differently. When that happens:

1. Keep the older file name (stable links), move the newer file's unique
   facts into it, and list both sources under `sources`.
2. Keep the strongest metric with its basis; note any conflicting number under
   `open_questions` instead of picking one silently.
3. Delete the newer file in the same commit and say so in the commit message.

The check-in agent runs a duplicate pass before every review PR.
