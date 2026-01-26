#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, RFPathError  # type: ignore

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
    ap = argparse.ArgumentParser(prog="rf_propose_changes")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Overwrite proposed-changes.md if it exists")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path
    pipe_dir = app / "resume_refs" / "resume_pipeline"
    job_json = pipe_dir / "job.json"
    sel_json = pipe_dir / "selection.json"
    emp_json = pipe_dir / "emphasis.json"

    for req in (job_json, sel_json, emp_json):
        if not req.exists():
            die(f"Missing required pipeline artifact: {req}")

    job = read_json(job_json)
    sel = read_json(sel_json)
    emp = read_json(emp_json)

    selected_slug = sel["selected"]["template_slug"]
    active_tags = emp.get("active_tags", [])

    out_path = pipe_dir / "proposed-changes.md"
    if out_path.exists() and not args.force:
        die(f"Refusing to overwrite existing: {out_path}\nUse --force if you intend to regenerate.")

    # Deterministic proposal set (v1)
    # Keep these generic and local. Agents can later propose more precise edits.
    proposals = []

    # Always include a “stack alignment” proposal based on selected template.
    proposals.append({
        "section": "SUMMARY",
        "change": "REPLACE",
        "from": "[PLACEHOLDER: existing summary line about primary stack]",
        "to": f"[PROPOSED: align summary to template stack: {selected_slug}]"
    })

    # Tag-driven proposals
    if "api" in active_tags:
        proposals.append({
            "section": "CORE COMPETENCIES",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add API testing emphasis: REST, Postman/Rest Assured, contract testing, response validation]"
        })

    if "cloud" in active_tags:
        proposals.append({
            "section": "CORE COMPETENCIES",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add cloud/devops emphasis: Docker, CI/CD pipelines, cloud test execution (AWS/Azure/GCP as relevant)]"
        })

    if "perf" in active_tags:
        proposals.append({
            "section": "CORE COMPETENCIES",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add performance emphasis: JMeter/k6, load/stress testing, latency/throughput metrics]"
        })

    if "etl" in active_tags:
        proposals.append({
            "section": "PROJECT EXPERIENCE",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add data pipeline/ETL validation emphasis: batch jobs, data integrity checks, warehouse validation]"
        })

    if "mobile" in active_tags:
        proposals.append({
            "section": "TOOLS",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add mobile automation emphasis: Appium, device lab testing, mobile regression strategy]"
        })

    if "ai_ml" in active_tags:
        proposals.append({
            "section": "PROJECT EXPERIENCE",
            "change": "ADD",
            "from": "",
            "to": "[PROPOSED: add AI/ML testing emphasis: model output validation, data quality checks, monitoring/alerting for drift (if applicable)]"
        })

    # Render markdown (locked format)
    lines = []
    lines.append("# Proposed Resume Changes (Numbered)")
    lines.append("")
    lines.append(f"- APP: {resolved.app_path}")
    lines.append(f"- FAMILY: {resolved.family}")
    lines.append(f"- SELECTED_TEMPLATE: {selected_slug}")
    lines.append(f"- GENERATED_UTC: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    n = 1
    for p in proposals:
        lines.append(f"{n})")
        lines.append(f"SECTION: {p['section']}")
        lines.append(f"CHANGE: {p['change']}")
        if p["change"] in ("REPLACE", "DELETE"):
            lines.append(f"FROM: {p['from']}")
        if p["change"] in ("REPLACE", "ADD"):
            lines.append(f"TO: {p['to']}")
        lines.append("")
        n += 1

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(out_path))

if __name__ == "__main__":
    main()
