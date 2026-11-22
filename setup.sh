#!/usr/bin/env bash
# setup.sh: make a new resume project from the sample person and install the plugin for it.
# Usage: ./setup.sh [--dry-run] <new project dir>
set -euo pipefail
DRY=0; [ "${1:-}" = "--dry-run" ] && { DRY=1; shift; }
DEST="${1:?usage: ./setup.sh [--dry-run] <new project dir>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
run(){ if [ $DRY = 1 ]; then echo "+ $*"; else "$@"; fi; }
command -v python3 >/dev/null || { echo "needs python3"; exit 1; }
command -v claude >/dev/null || { echo "needs Claude Code: https://code.claude.com"; exit 1; }
[ -e "$DEST" ] && { echo "$DEST already exists"; exit 1; }
run cp -R "$HERE/sample" "$DEST"
run cp "$HERE/templates/CLAUDE-snippet.md" "$DEST/CLAUDE.md"
run git -C "$DEST" init -q
( [ $DRY = 1 ] && echo "+ cd $DEST" ) || cd "$DEST"
run claude plugin marketplace add "$HERE" --scope project
run claude plugin install agentic-resume@agentic-resume --scope project
echo "Done. Next: cd $DEST && claude, then say: make this my resume"
