#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, RFPathError  # type: ignore


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_propose_changes_ai")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    ap.add_argument(
        "--rr-occurrence",
        type=int,
        default=1,
        help="1-indexed Roles and Responsibilities occurrence (default: 1)",
    )
    args, extra = ap.parse_known_args()

    try:
        _resolved = resolve_app(args.app, root=args.root)  # validation + consistent errors
    except RFPathError as e:
        die(str(e))

    runner = Path("~/secondbrain/01_projects/resume-factory/scripts/rf_agent_runner.py").expanduser()
    if not runner.exists():
        die(f"Missing rf_agent_runner.py: {runner}")

    cmd = [
        sys.executable,
        str(runner),
        "--mode",
        "propose",
        "--app",
        args.app,
        "--root",
        args.root,
        "--rr-occurrence",
        str(args.rr_occurrence),
    ]
    if args.force:
        cmd.append("--force")

    # forward unknown args for future compatibility
    cmd += extra

    r = subprocess.run(cmd)
    raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
