#!/usr/bin/env python3
"""Eval harness, part 1: prove the hard checks are valid.

A check is only useful if it passes good output and fails bad output. This
copies the sample person to a temp folder, writes a hand-checked good resume
(must pass every check), then plants one failure at a time (each must be
caught by the right check, and only fail where expected).

Usage: python3 evals-harness/run.py [--keep]
Exit 0 only if every case behaves as expected.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.dirname(HERE)
BIN = os.path.join(REPO, "plugins", "agentic-resume", "bin")
SAMPLE = os.path.join(REPO, "sample")
EM = chr(0x2014)

GOOD = [
    ("Cut checkout errors from 4.1 to 0.6 percent in 30 days by fixing a payment retry storm at a regional freight company.", "stories/2026-03-checkout-errors.md"),
    ("Rebuilt on-call at a health tech startup, cutting pages from 14 to 3 a week.", "stories/2025-09-on-call-rotation.md"),
    ("Built one-click deploys that cut deploy time from 45 to 8 minutes and moved releases from weekly to daily.", "stories/2025-04-deploy-pipeline.md"),
    ("Wrote a setup CLI that cut new-engineer setup from about 2 days to 2 hours.", "stories/2026-01-internal-cli.md"),
]


def write_resume(root, items):
    os.makedirs(os.path.join(root, "resume"), exist_ok=True)
    body = ["# Alex Rivera", "alex@example.com", "", "Platform engineer.", "", "## Experience", "",
            "### A regional freight company", "**Platform Engineer** | Oct 2025 to Present", ""] + [f"- {b}" for b, _ in items] + [
            "", "## Education", "", "Software engineering bootcamp, 2024", "", "## Skills", "", "Python, AWS, CI/CD"]
    open(os.path.join(root, "resume", "resume.md"), "w").write("\n".join(body) + "\n")
    trace = ["# Resume trace (private)", ""] + [f"{i}. {p}" for i, (_, p) in enumerate(items, 1)]
    open(os.path.join(root, "profile", "resume-trace.md"), "w").write("\n".join(trace) + "\n")


def run(cmd, root):
    env = dict(os.environ, AR_PROJECT_ROOT=root)
    r = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def fresh(tmp, name):
    root = os.path.join(tmp, name)
    shutil.copytree(SAMPLE, root)
    write_resume(root, GOOD)
    return root


def bullets(mutate):
    items = [list(x) for x in GOOD]
    mutate(items)
    return [tuple(x) for x in items]


CASES = [
    # name, how to plant the failure, which tool must fail, text expected in its output
    ("clean resume passes every check", None, None, None),
    ("invented number", lambda r: write_resume(r, bullets(lambda b: b[0].__setitem__(0, b[0][0].replace("0.6", "0.2")))), "ar-trace", "not found"),
    ("em dash", lambda r: write_resume(r, bullets(lambda b: b[1].__setitem__(0, b[1][0].replace(", cutting", f" {EM} cutting")))), "ar-lint", "dash"),
    ("client name in public resume", lambda r: write_resume(r, bullets(lambda b: b[0].__setitem__(0, b[0][0].replace("a regional freight company", "SAMPLE-CLIENT-A")))), "ar-guard", "SAMPLE-CLIENT-A"),
    ("client name only in a public file name", lambda r: open(os.path.join(r, "site", "sample-client-a-notes.md"), "w").write("notes\n"), "ar-guard", "in path"),
    ("blocked term in site", lambda r: open(os.path.join(r, "site", "about.md"), "w").write("We built SAMPLE-PRIVATE-TERM.\n"), "ar-guard", "SAMPLE-PRIVATE-TERM"),
    ("banned word", lambda r: write_resume(r, bullets(lambda b: b[2].__setitem__(0, "Spearheaded one-click deploys that cut deploy time from 45 to 8 minutes."))), "ar-lint", "spearheaded"),
    ("casual word in professional text", lambda r: write_resume(r, bullets(lambda b: b[3].__setitem__(0, b[3][0] + " lol"))), "ar-lint", "lol"),
    ("bullet too long", lambda r: write_resume(r, bullets(lambda b: b[1].__setitem__(0, b[1][0] + " The rotation also covered weekends, holidays, release nights, vendor outages, database maintenance windows and every single customer escalation."))), "ar-lint", "max 25"),
    ("bullet does not start with a verb", lambda r: write_resume(r, bullets(lambda b: b[1].__setitem__(0, "I rebuilt on-call at a health tech startup, cutting pages from 14 to 3 a week."))), "ar-lint", "start with a verb"),
    ("invented number outside the bullets", lambda r: open(os.path.join(r, "resume", "resume.md"), "a").write("\nTechnical owner for 75 enterprise accounts.\n"), "ar-trace", "not found in any cited story"),
    ("story file name in public resume", lambda r: write_resume(r, bullets(lambda b: b[0].__setitem__(0, b[0][0] + " See 2026-03-checkout-errors."))), "ar-trace", "file name"),
    ("bullet with no trace entry", lambda r: open(os.path.join(r, "profile", "resume-trace.md"), "w").write("1. stories/2026-03-checkout-errors.md\n"), "ar-trace", "no trace entry"),
    ("never-public story used", lambda r: write_resume(r, bullets(lambda b: b.append(("Built a prototype for an interview.", "stories/2026-05-private-interview-exercise.md")))), "ar-trace", "never_public"),
    ("secret in a file", lambda r: open(os.path.join(r, "profile", "notes.md"), "w").write("key=AKIA" + "ABCDEFGHIJKLMNOP" + "\n"), "ar-secrets", "aws_access_key"),
]


def main():
    tmp = tempfile.mkdtemp(prefix="ar-harness-")
    tools = ["ar-guard", "ar-secrets", "ar-lint", "ar-trace"]
    results, ok_all = [], True
    for i, (name, plant, tool, expect) in enumerate(CASES):
        root = fresh(tmp, f"case{i:02d}")
        if plant:
            plant(root)
        outs = {}
        for t in tools:
            cmd = [os.path.join(BIN, t)] + ([root] if t == "ar-secrets" else ["--root", root])
            if t == "ar-lint":
                cmd.append(os.path.join(root, "resume", "resume.md"))
            outs[t] = run(cmd, root)
        failed = [t for t, (code, _) in outs.items() if code != 0]
        if tool is None:
            ok = not failed
        else:
            ok = failed == [tool] and expect.lower() in outs[tool][1].lower()
        ok_all &= ok
        results.append((name, tool or "all pass", ", ".join(failed) or "none", "PASS" if ok else "WRONG"))
    # ranking excludes never-public stories
    code, out = run([os.path.join(BIN, "ar-rank"), "--root", fresh(tmp, "rank"), "--no-write"], SAMPLE)
    ok = code == 0 and "private-interview" not in out
    ok_all &= ok
    results.append(("ranking skips never-public stories", "ar-rank", "none" if code == 0 else "ar-rank", "PASS" if ok else "WRONG"))
    # the hook blocks a commit (exit 2) when a check fails
    root = fresh(tmp, "hook")
    write_resume(root, bullets(lambda b: b[0].__setitem__(0, b[0][0].replace("a regional freight company", "SAMPLE-CLIENT-A"))))
    r = subprocess.run([os.path.join(BIN, "ar-hook-precommit")], cwd=root, env=dict(os.environ, CLAUDE_PROJECT_DIR=root), capture_output=True, text=True)
    ok = r.returncode == 2 and "SAMPLE-CLIENT-A" in r.stderr
    ok_all &= ok
    results.append(("hook blocks a failing commit (exit 2)", "ar-hook-precommit", f"exit {r.returncode}", "PASS" if ok else "WRONG"))
    root = fresh(tmp, "hook-clean")
    r = subprocess.run([os.path.join(BIN, "ar-hook-precommit")], cwd=root, env=dict(os.environ, CLAUDE_PROJECT_DIR=root), capture_output=True, text=True)
    ok = r.returncode == 0
    ok_all &= ok
    results.append(("hook allows a clean commit (exit 0)", "ar-hook-precommit", f"exit {r.returncode}", "PASS" if ok else "WRONG"))
    # intake writes a valid entry
    root = fresh(tmp, "intake")
    code, out = run([os.path.join(BIN, "ar-add-entry"), "--root", root, "--source", "cli", "--kind", "win", "--when", "2026-06-03T10:00", "Closed 5 of 6 action items"], root)
    entry = os.path.join(root, out.strip())
    ok = code == 0 and os.path.exists(entry) and "kind: win" in open(entry).read()
    code2, _ = run([os.path.join(BIN, "ar-add-entry"), "--root", root, "--source", "cli", "--kind", "correction", "x"], root)
    ok = ok and code2 != 0
    ok_all &= ok
    results.append(("intake writes a valid entry, rejects a correction without --corrects", "ar-add-entry", "none", "PASS" if ok else "WRONG"))

    # ATS: a clean, standard resume passes; a missing Experience heading or a table fails
    ats_ok = "# Alex Rivera\nalex@example.com\n\n## Experience\n\n### A regional freight company\n**Platform Engineer** | Oct 2025 to Present\n\n- Cut checkout errors from 4.1 to 0.6 percent.\n\n## Education\n\nBootcamp, 2024\n\n## Skills\n\nPython, AWS\n"
    for label, body, want in (("ATS: standard resume passes", ats_ok, 0),
                              ("ATS: missing Experience heading fails", ats_ok.replace("## Experience", "## Work"), 1),
                              ("ATS: a table fails", ats_ok + "\n| a | b |\n|---|---|\n", 1)):
        root = fresh(tmp, "ats" + str(want) + str(len(body)))
        fpath = os.path.join(root, "resume", "ats-test.md"); open(fpath, "w").write(body)
        code, out = run([os.path.join(BIN, "ar-ats"), "--root", root, "--resume", fpath], root)
        ok = (code == 0) == (want == 0)
        ok_all &= ok
        results.append((label, "ar-ats", f"exit {code}", "PASS" if ok else "WRONG"))

    w = max(len(r[0]) for r in results)
    print(f"{'case'.ljust(w)} | must fail     | failed                 | result")
    for name, tool, failed, res in results:
        print(f"{name.ljust(w)} | {tool.ljust(13)} | {failed.ljust(22)} | {res}")
    print(f"\n{sum(r[3] == 'PASS' for r in results)} of {len(results)} cases behave as expected")
    if "--keep" not in sys.argv:
        shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
