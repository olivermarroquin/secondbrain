#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# local lib import (no installs, deterministic)
LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, list_templates, RFPathError  # type: ignore

REQUIRED_REL_FILES = [
    "jd/jd-raw.txt",
    "tracking/job-meta.json",
    "tracking/application-record.json",
]

OPTIONAL_REL_FILES = [
    "jd/job-post-url.txt",
]

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def read_json(p: Path):
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_load_job")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--write-debug", action="store_true", help="Write resume_refs/resume_pipeline/job.json")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path

    missing = []
    for rel in REQUIRED_REL_FILES:
        if not (app / rel).exists():
            missing.append(rel)
    if missing:
        die("Missing required files under APP:\n  - " + "\n  - ".join(missing))

    jd_raw_path = app / "jd/jd-raw.txt"
    jd_raw = read_text(jd_raw_path).strip()
    if not jd_raw:
        die("jd/jd-raw.txt is empty")

    job_meta = read_json(app / "tracking/job-meta.json")
    app_record = read_json(app / "tracking/application-record.json")

    job_post_url = None
    url_path = app / "jd/job-post-url.txt"
    if url_path.exists():
        job_post_url = read_text(url_path).strip() or None

    # Template inventory (read-only)
    templates = list_templates(resolved)
    template_inventory = []
    for tdir in templates:
        template_inventory.append({
            "template_dir": str(tdir),
            "resume_master_docx": str(tdir / "resume-master.docx"),
            "signals_json": str(tdir / "signals.json") if (tdir / "signals.json").exists() else None,
        })

    payload = {
        "schema": "rf_job_v1",
        "loaded_at_utc": datetime.now(timezone.utc).isoformat(),

        "app": {
            "app_path": str(resolved.app_path),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },

        "paths": {
            "jobs_root": str(resolved.jobs_root),
            "templates_root": str(resolved.templates_root),
            "outputs_root": str(resolved.outputs_root),
        },

        "inputs": {
            "jd_raw_path": str(jd_raw_path),
            "job_post_url": job_post_url,
            "job_meta_path": str(app / "tracking/job-meta.json"),
            "application_record_path": str(app / "tracking/application-record.json"),
        },

        "job_meta": job_meta,
        "application_record": app_record,
        "jd_raw": jd_raw,

        "template_inventory": template_inventory,
    }

    if args.write_debug:
        out_dir = app / "resume_refs" / "resume_pipeline"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "job.json"
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(str(out_path))
    else:
        print(json.dumps(payload, ensure_ascii=False))

if __name__ == "__main__":
    main()
