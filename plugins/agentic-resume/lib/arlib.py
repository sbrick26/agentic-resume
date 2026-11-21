"""Shared helpers for the agentic-resume tools. Standard library only.

A project (the user's own repo) is laid out by convention:
  stories/*.md              one story per file, YAML-style front matter
  career-log/inbox/*.md     new updates waiting to be processed
  profile/                  private resume source data and the resume trace
  writing-style/STYLE.md    the user's writing style, with a "Words to avoid" section
  privacy/                  client-names.txt, blocklist.txt, public-paths.txt (private)
  resume/                   public output only
"""
import os
import re
import glob

EN_DASH, EM_DASH = chr(0x2013), chr(0x2014)


def project_root(arg=None):
    return os.path.abspath(arg or os.environ.get("AR_PROJECT_ROOT") or os.getcwd())


def _scalar(v):
    v = v.strip()
    if v.startswith('"') and v.endswith('"') and len(v) >= 2:
        return bytes(v[1:-1], "utf-8").decode("unicode_escape") if "\\" in v else v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in re.findall(r'"(?:[^"\\]|\\.)*"|[^,]+', inner)]
    return v


def front_matter(text):
    """Parse the simple front matter these tools write: scalars, one level of
    nesting, inline lists, and lists of small maps. Returns (dict, body)."""
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return {}, text
    data, key, item = {}, None, None
    for raw in m.group(1).split("\n"):
        line = raw.split("  #")[0].rstrip() if not raw.strip().startswith('"') else raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0 and ":" in s:
            k, v = s.split(":", 1)
            key, item = k.strip(), None
            data[key] = _scalar(v) if v.strip() else {}
        elif s.startswith("- ") and key is not None:
            if not isinstance(data[key], list):
                data[key] = []
            item = {}
            data[key].append(item)
            if ":" in s[2:]:
                k, v = s[2:].split(":", 1)
                item[k.strip()] = _scalar(v)
        elif ":" in s and key is not None:
            k, v = s.split(":", 1)
            if item is not None and isinstance(data[key], list):
                item[k.strip()] = _scalar(v)
            elif isinstance(data[key], dict):
                data[key][k.strip()] = _scalar(v)
    return data, m.group(2)


def load_stories(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, "stories", "*.md"))):
        name = os.path.basename(p)
        if name.startswith("_") or name.isupper() or name in ("README.md", "INDEX.md"):
            continue
        text = open(p, encoding="utf-8").read()
        fm, body = front_matter(text)
        if not fm:
            continue
        out.append({"path": os.path.relpath(p, root), "fm": fm, "body": body, "text": text})
    return out


def score(fm):
    s = fm.get("scores") or {}
    parts = [s.get(k) for k in ("impact", "metric_strength", "role_fit", "recency")]
    if all(isinstance(x, int) for x in parts):
        return sum(parts), s.get("impact", 0)
    return s.get("total", 0) or 0, s.get("impact", 0) or 0


def _lines(path):
    if not os.path.exists(path):
        return []
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]


def client_names(root):
    """[(name, generic)] from privacy/client-names.txt, longest name first."""
    pairs = []
    for l in _lines(os.path.join(root, "privacy", "client-names.txt")):
        name, _, generic = l.partition("|")
        if name.strip():
            pairs.append((name.strip(), generic.strip() or "a client"))
    return sorted(pairs, key=lambda x: -len(x[0]))


def blocked_terms(root):
    terms = [t.strip() for t in _lines(os.path.join(root, "privacy", "blocklist.txt"))]
    return sorted(set(terms + [n for n, _ in client_names(root)]), key=str.lower)


def public_paths(root):
    return [p.strip() for p in _lines(os.path.join(root, "privacy", "public-paths.txt"))]


def term_hits(text, term):
    """Case-insensitive whole-word literal match; returns 1-based line numbers."""
    rx = re.compile(r"(?<![\w])" + re.escape(term) + r"(?![\w])", re.I)
    return [i for i, line in enumerate(text.splitlines(), 1) if rx.search(line)]


def banned_words(root):
    """Words from the "Words to avoid" section of writing-style/STYLE.md."""
    path = os.path.join(root, "writing-style", "STYLE.md")
    if not os.path.exists(path):
        return [], []
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^## Words to avoid\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return [], []
    block = m.group(1)
    casual = []
    cm = re.search(r"also:\s*(.*?)(?:\.\s|\n\n|$)", block, re.S)
    first_para = block.strip().split("\n\n")[0]
    words = [re.sub(r"\(.*?\)", "", w).strip().strip(".") for w in first_para.replace("\n", " ").split(",")]
    if cm:
        casual = [w.strip().strip(".") for w in cm.group(1).replace("\n", " ").split(",")]
        casual = [w for w in casual if w and len(w.split()) <= 2]
    return [w for w in words if w], casual
