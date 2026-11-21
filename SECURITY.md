# Security

Plugins run with your user permissions. This is everything this plugin
runs, so you can review it.

- **Hook**: hooks/hooks.json runs bin/ar-hook-precommit before Claude runs
  `git commit` or `git push`. It runs ar-check and blocks the command (exit
  2) if a check fails. It reads your project files; it writes nothing.
- **bin/**: ar-add-entry writes one file to career-log/inbox/. ar-rank writes
  stories/INDEX.md. ar-guard, ar-trace, ar-lint, ar-secrets and ar-check only
  read. None of them use the network.
- **No MCP servers, no monitors, no background processes.**
- **Untrusted text**: inbox entries, notes and web pages are treated as
  data. Agents that read them have no write access outside the project and
  no network tools.
- **Secrets**: the plugin never asks for or stores keys. Keep yours in your
  OS keychain or CI secrets.

Pin a tagged version in your project's .claude/settings.json and keep
auto-update off, so a new version only arrives when you review it.

Report a vulnerability through a private security advisory on this repo.
