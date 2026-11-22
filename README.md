# agentic-resume

**Tell Claude what you did at work. Get a resume that stays current, fits one
page, passes ATS scans, and never makes things up.**

It is a free resume builder that runs inside Claude Code (Anthropic's AI
coding assistant). No website, no account, no upload: your career data stays
in a folder on your computer.

## Try it in 3 steps

1. Install Claude Code: https://code.claude.com
2. Get this repo and open Claude in it:
   ```bash
   git clone https://github.com/sbrick26/agentic-resume
   cd agentic-resume
   claude
   ```
3. Type: **"Set me up."**

Claude checks your machine, makes your own private resume folder, reads your
current resume (paste it or point to the file), and writes your first
version with every check run. To just look around first, it starts with a
made-up sample person, Alex Rivera.

## What you get

- **A daily habit, not a yearly scramble.** Tell Claude what you shipped
  ("cut deploy time from 45 to 8 minutes"). It files each update as a story
  with its numbers, and keeps your resume and site copy up to date.
- **Nothing invented.** Every resume line traces to one of your stories,
  and every number in it must be in that story.
- **One page, checked.** It renders the page and tells you exactly which
  lines to trim.
- **Scanned like a recruiter would.** A mock ATS parse (headings, dates,
  contact line, keywords, hidden text) and optional mock AI screeners that
  read your resume against a real job posting.
- **Private stays private.** Client names you list never appear in anything
  public; your chosen generic wording is used instead.
- **Your voice.** You edit a shared page; your final version becomes the
  reference every later draft matches.

## How it works

```
you: "shipped X today"  ->  inbox note  ->  story (numbers + where they came from)
        ->  ranked  ->  resume and site copy  ->  checks: trace, one page, ATS, privacy
        ->  you review and approve
```

It is packaged as a Claude Code plugin (skills, agents and small check
scripts). `setup.sh` installs it for your folder; you never need to call the
pieces yourself, but you can (see below).

## Your project layout

| Folder | What | Public? |
|---|---|---|
| stories/ | one story per piece of work | no |
| career-log/inbox/ | new updates waiting to be filed | no |
| profile/ | jobs, education, target role, resume trace | no |
| writing-style/STYLE.md | how you write (start from templates/STYLE.md) | no |
| privacy/ | client names with generic wording, blocked terms | no |
| resume/, site/ | generated output | yes |

## Skills

checkin, process-inbox, rank-stories, write-resume, write-site-copy,
style-check, review-pr, review-message, improve-site, maintain,
improve-engine. Run any of them as `/agentic-resume:<name>`.

## Agents

resume-writer (Opus), archivist (Sonnet), eval-grader (Sonnet, never the
same model as the writer), qa (Haiku), site-designer (Opus, read-only).

## Checks (bin/, on the Bash path inside Claude Code)

| Tool | Fails on |
|---|---|
| ar-guard | a client name or blocked term in a public path (contents or file names) |
| ar-trace | a bullet with no story, a number not in its story, a story file name in public output |
| ar-lint | em or en dashes, words you listed to avoid, long or verbless bullets |
| ar-secrets | API keys, tokens, private keys |
| ar-ats | missing standard headings, tables, images, a missing contact line, hidden text or prompt injection; reports odd or overlapping dates, low keyword coverage (profile/target-keywords.txt) and skills never shown in a bullet |
| ar-fit | not fitting one page: renders in headless Chrome at 10.5pt then 10pt and names the cheapest lines to trim (skipped without Chrome) |
| ar-check | any of the above, plus gitleaks if installed |
| ar-doctor | checks the machine and project (Python, Chrome, claude CLI, folders, settings); installs nothing |

## Settings

Optional `agentic-resume.json` at your project root:

```json
{"max_bullet_words": 25, "page": "letter", "min_font_pt": 10, "max_pages": 1}
```

## Editing with the user

The `working-page` skill is how the resume gets from a good draft to the one
the owner loves: a shared page, one suggestion per line, a fit and ATS check
after every round, and the owner's final edit saved as the golden reference
(writing-style/REFERENCE-RESUME.md) that later drafts match. The research
behind each check is in docs/RESEARCH.md.

## Evals

```bash
python3 evals-harness/run.py
```

Plants one failure at a time in a copy of the sample (invented number, dash,
client name, banned word, missing trace, secret, and more) and checks that
exactly the right tool catches it, and that a clean resume passes. Graded
evals (accuracy and style, scored by a different model than the writer) are
in plugins/agentic-resume/evals/.

## What it never does

No network calls except Claude itself. No MCP servers. It never writes a
listed client name to a public path, never merges or deploys on its own,
and never stores your data in the plugin. See SECURITY.md for every hook and
script.

## License

MIT
