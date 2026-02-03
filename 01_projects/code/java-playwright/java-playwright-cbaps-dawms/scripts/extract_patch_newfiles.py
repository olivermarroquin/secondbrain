#!/usr/bin/env python3
import sys, re
from pathlib import Path

patch_path = Path(sys.argv[1]).expanduser()
out_root = Path(sys.argv[2]).expanduser()

if not patch_path.exists():
    print(f"Missing patch: {patch_path}", file=sys.stderr)
    sys.exit(1)

out_root.mkdir(parents=True, exist_ok=True)

current_file = None
buf = []

def flush():
    global current_file, buf
    if current_file is None:
        return
    dest = out_root / current_file
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("".join(buf), encoding="utf-8")
    current_file = None
    buf = []

re_file = re.compile(r'^\+\+\+ b/(.+)$')

with patch_path.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        m = re_file.match(line.rstrip("\n"))
        if m:
            flush()
            current_file = m.group(1)
            continue

        if current_file is not None:
            if line.startswith("+") and not line.startswith("+++"):
                buf.append(line[1:])
            elif line.startswith("\\ No newline"):
                pass
            elif line.startswith("diff --git "):
                flush()

flush()
print(f"Extracted files into: {out_root}")

