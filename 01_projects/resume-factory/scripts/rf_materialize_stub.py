#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_materialize_stub (STUB)")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    app = Path(args.app).expanduser().resolve()
    pipe = app / "resume_refs" / "resume_pipeline"
    pipe.mkdir(parents=True, exist_ok=True)

    out_patches = pipe / "patches.json"
    if out_patches.exists() and not args.force:
        die(f"Refusing to overwrite existing patches.json (use --force): {out_patches}")

    stub = {
        "schema": "rf_patches_v1",
        "built_at_utc": now_utc(),
        "app": {
            "app_path": str(app),
            "family": "STUB",
            "company": "STUB",
            "role_slug": "STUB",
        },
        "approved_change_numbers": [],
        "patches": [],
    }

    out_patches.write_text(json.dumps(stub, indent=2) + "\n", encoding="utf-8")
    print(str(out_patches))


if __name__ == "__main__":
    main()
