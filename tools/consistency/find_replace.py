import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGETS = list(ROOT.rglob("*.md"))
REPLACEMENTS = [
    (r"\\bSecond Story Services\\b", "2nd Story Services"),
    (r"\\bSecond Story\\b", "2nd Story"),
    (r"\\b2ndStory\\b", "2nd Story"),
]
changed = 0
for p in TARGETS:
    s = p.read_text(encoding="utf-8")
    orig = s
    for pat, repl in REPLACEMENTS:
        s = re.sub(pat, repl, s)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        changed += 1
print(f"Updated {changed} files.")
