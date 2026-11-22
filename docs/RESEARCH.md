# Research behind the checks (2026-11-22)

What real screening does, and how each finding shows up in the engine.
Severities follow the least capable parser. Vendor figures are directional.

## How ATS parsers read a resume

| Finding | Engine rule | Source |
|---|---|---|
| Textkernel (used by SuccessFactors; owns Sovren) lists coded quality findings. Fatal: data in columns (433), no sections (412), no work history (413), no education (414), jobs without dates (419), date range over several lines (418), no email and no phone (441). | ar-ats: standard headings, a one-line date range per role, email or phone near the top; ar-fit renders a single column | https://developer.textkernel.com/tx-platform/v10/resume-parser/overview/parser-output |
| Taleo recruiter search is exact match by default, so an acronym does not match its long form. | Writer: spell out once, "watsonx Orchestrate (WXO)" | https://docs.oracle.com/en/cloud/saas/taleo-enterprise/otrcg/c-advancedsearchkeywords.html |
| "2020 to Present" is a documented input for RChilli; "to" is fine. | ar-ats accepts "to", "-" and "through" | https://help.rchilli.com/hc/en-us/articles/4404204581145 |
| Greenhouse does not auto-reject on match; rejection comes from employer knockouts. | Keyword coverage is a warning, never a fail on its own | https://support.greenhouse.io/hc/en-us/articles/41131886674075 |
| About 1% of resumes carry hidden prompts or white text; recruiters reject for it. | ar-ats fails zero-width characters, white or tiny text, instruction-like strings | https://builtin.com/articles/hidden-ai-prompts-in-resume |
| Text PDFs are accepted by Greenhouse, Workday HiredScore, Taleo and Textkernel. | PDF output is fine; it must have a text layer | https://support.greenhouse.io/hc/en-us/articles/360052218132 |

Myths not encoded: "75% of resumes are rejected by ATS" (a 2013 sales pitch,
https://fortune.com/2014/08/22/how-to-keep-your-resume-from-getting-lost-in-cyberspace/);
"PDFs always fail"; "one page is mandatory"; "'to' in dates breaks parsing";
fixed vendor-to-engine mappings.

## How AI screeners judge

| Finding | Engine rule | Source |
|---|---|---|
| Workday HiredScore, Ashby and Greenhouse grade each required and preferred criterion as met or not, with evidence; they do not free-rank. | ai-screen: criteria checklist with quoted evidence, not one free score | https://docs.ashbyhq.com/ai-assisted-application-review |
| LLM judges prefer resumes written by their own model (67 to 82 percent). | Screen with a model family other than the writer's when available; report it when not | https://arxiv.org/abs/2509.00462 |
| 21 of 22 LLMs prefer the first candidate shown. | Swap order in any pairwise comparison | https://arxiv.org/abs/2505.17049 |
| Three LLMs disagreed on 39 percent of resumes. | Several runs and models; report spread and disagreement, not an average | https://arxiv.org/pdf/2603.18390 |
| Judge scores can rise through formatting with no human gain. | Code gates first; rerun format-only variants; calibrate against the owner's labels | https://arxiv.org/html/2507.05619v2 |
| Recruiters filter by skill keywords and title first (vendor survey). | ar-ats keyword coverage; skills shown in bullets, not only listed | https://www.jobscan.co/state-of-the-job-search |

## Page and writing

- Career centers: 10 to 12pt body, margins at least 0.5in (Duke, Emerson, BU);
  Cornell sets 10.5pt as a floor. ar-fit tries 10.5pt first and warns below it.
  https://careers.bu.edu/resources/resumes/
- Ladders eye tracking (2018, vendor): simple single column, clear job titles,
  bulleted accomplishments, keywords in context.
  https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/
- One versus two pages is split among recruiters (ResumeGo, Accountemps); one
  page is the default here, and never padded to two.
  https://resumego.net/research/one-or-two-page-resumes
- Bullet length, bullets per role and sub-bullets have no rigorous study;
  the engine treats them as conventions the owner's directives can override.

## Prior art

Resume-Matcher (Apache-2.0): code-only ATS checks on the extracted PDF text.
RenderCV (MIT): YAML with a JSON Schema, Typst rendering. Reactive Resume
(MIT): JSON Resume import and export. JSON Resume schema: the common exchange
format. None traces claims to source stories or guards private names, which
is what this engine adds. https://github.com/srbhr/Resume-Matcher ,
https://github.com/rendercv/rendercv , https://jsonresume.org/schema

## Next, before a public release

1. Bundle Carlito (SIL OFL, metric-compatible with Calibri) so ar-fit gives the
   same line breaks on every machine; record the Chrome version in results.
2. Check the rendered PDF itself: text layer, extracted text order, glyphs.
3. `doctor` script: Python 3.10+, Chrome or Chromium, `claude` CLI; prints
   install hints, installs nothing.
4. `userConfig` for the stories folder, page size (letter or A4) and minimum
   font size; caches in `${CLAUDE_PLUGIN_DATA}`.
5. JSON Resume export (and import to bootstrap a profile).
6. ai-screen as a per-criterion checklist with evidence; model family note.
7. claude.ai and Cowork do not install plugins with a top-level `bin/`; move
   scripts to `scripts/` if those surfaces matter.
Sources: https://code.claude.com/docs/en/plugins-reference ,
https://github.com/googlefonts/carlito
