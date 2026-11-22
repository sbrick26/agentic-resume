# agentic-resume

A Claude Code plugin that turns your career stories into a resume and site
copy in your own writing style, and proves it with evals.

- **Stories in.** Every update (a daily check-in, a win, a note) lands as a
  dated entry; Claude files it into one story per piece of work and scores
  it on impact, metric strength, role fit and recency.
- **Resume out.** The best stories become resume bullets in your voice.
  Every bullet traces to a story, and every number in it must appear there.
- **Private stays private.** Client names you list are never written to
  public output; the generic wording you choose is used instead.
- **Evals included.** A harness proves each check catches what it should,
  and graded evals score accuracy and style.

## Quick start (60 seconds)

```bash
git clone <this repo> agentic-resume
cd agentic-resume
./setup.sh ~/my-resume          # makes a project from the sample person
cd ~/my-resume && claude        # then try: /agentic-resume:rank-stories
```

`setup.sh` copies the sample person into a new folder, adds this repo as a
plugin marketplace, and installs the plugin for that project. It asks for
nothing except Claude access (your Anthropic API key or a Claude plan that
includes Claude Code). Run `./setup.sh --dry-run <dir>` to see every command
first.

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
| ar-ats | missing standard headings, tables, images, odd date ranges, over one page, low keyword coverage (profile/target-keywords.txt) |
| ar-check | any of the above, plus gitleaks if installed |

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
