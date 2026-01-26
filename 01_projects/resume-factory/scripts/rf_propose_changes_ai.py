#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
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
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        die(f"Missing required file: {p}")


def load_json(p: Path) -> dict:
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def _extract_company_role_from_app(app: Path) -> tuple[str, str]:
    # APP = .../01_projects/jobs/<family>/<company>/<role_slug>
    parts = app.parts
    if len(parts) < 3:
        return "unknown", "unknown"
    return parts[-2], parts[-1]


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _stub_generate_real_proposals(
    family: str,
    selected_slug: str,
    emphasis_tags: list[str],
    jd_text: str,
    rr_occurrence: int,
) -> list[dict]:
    """
    Deterministic non-AI proposal generator.
    Produces REAL resume-ready text; no placeholders.
    """
    jd = jd_text.lower()

    proposals: list[dict] = []

    # 1) SUMMARY replace-section: align to template stack and JD cues
    stack_line = {
        "01_java_selenium": "Senior QA Automation Engineer with 7+ years building Java/Selenium frameworks, CI-driven regression suites, and API/data validation for enterprise systems.",
        "02_java_playwright_migration": "Senior QA Automation Engineer with 7+ years modernizing UI automation, including Selenium→Playwright migration, scalable Java frameworks, and CI-driven execution.",
        "03_python_playwright": "Senior QA Automation Engineer with 7+ years building Python/Pytest automation, Playwright-based UI suites, and API/data validation in CI pipelines.",
        "04_typescript_playwright": "Senior QA Automation Engineer with 7+ years delivering Playwright E2E automation in TypeScript/JavaScript, reliable CI pipelines, and API/data validation for high-traffic products."
    }.get(selected_slug, f"Senior {family.replace('_',' ').title()} with strong automation and delivery focus.")

    summary_lines = [
        stack_line,
        "Strengths include API testing, SQL validation, risk-based test strategy, and cross-functional delivery in Agile/Scrum teams.",
        "Known for stabilizing flaky suites, improving coverage on critical workflows, and producing decision-ready QA reporting."
    ]

    proposals.append({
        "section": "SUMMARY",
        "change": "REPLACE_SECTION",
        "to_paragraphs": summary_lines
    })

    # 2) TECHNICAL SKILL adds (fallback-safe): map emphasis tags to concrete content
    tag_to_lines = {
        "api": "API Testing: REST, Postman, contract testing, response/schema validation, chaining workflows.",
        "cloud": "CI/CD & Cloud: Dockerized test runs, GitHub Actions/Jenkins, cloud execution (AWS/Azure/GCP as applicable).",
        "perf": "Performance: JMeter/k6 load/stress, latency/throughput metrics, bottleneck analysis and reporting.",
        "etl": "Data/ETL: SQL validation, ETL pipeline checks, reconciliation queries, dashboard/data quality verification.",
        "mobile": "Mobile: Cross-device validation, responsive testing, mobile web workflows, emulator/device smoke coverage.",
        "ai_ml": "AI/ML: Data quality checks, validation of model outputs against expected behaviors, monitoring/alerting signals."
    }

    for t in emphasis_tags:
        if t in tag_to_lines:
            proposals.append({
                "section": "TECHNICAL SKILL",
                "change": "ADD",
                "to": tag_to_lines[t]
            })

    # 3) PROJECT EXPERIENCE / Roles and Responsibilities: add 1 bullet under chosen RR occurrence
    # Only if emphasis suggests it; keep it tight.
    rr_lines = []
    if "api" in emphasis_tags:
        rr_lines.append("• Expanded automated coverage with API validation (status codes, payload assertions, negative cases) to reduce regression risk on critical workflows.")
    if "cloud" in emphasis_tags:
        rr_lines.append("• Integrated automation into CI pipelines (gated runs, artifacts, reports) to improve release confidence and feedback speed.")
    if "perf" in emphasis_tags:
        rr_lines.append("• Added performance checks (baseline latency/throughput) and reporting to surface bottlenecks before release.")

    if rr_lines:
        proposals.append({
            "section": "PROJECT EXPERIENCE",
            "change": "ADD",
            "subsection": "ROLES_AND_RESPONSIBILITIES",
            "subsection_occurrence": rr_occurrence,
            "to": "\n".join(rr_lines[:2])  # cap to 2 bullets
        })

    return proposals


def _write_proposed_changes_md(out_path: Path, resolved, selected_slug: str, proposals: list[dict]) -> None:
    lines: list[str] = []
    lines.append("# Proposed Resume Changes (AI)")
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
        if p.get("subsection"):
            lines.append(f"SUBSECTION: {p['subsection']}")
        if p.get("subsection_occurrence") is not None:
            lines.append(f"SUBSECTION_OCCURRENCE: {p['subsection_occurrence']}")

        if p["change"] == "REPLACE_SECTION":
            # prefer to_paragraphs
            paras = p.get("to_paragraphs")
            if not isinstance(paras, list) or not paras:
                die("REPLACE_SECTION requires to_paragraphs[] in AI proposer v1")
            lines.append("TO:")
            for s in paras:
                lines.append(f"- {_clean(str(s))}")
        elif p["change"] == "ADD":
            lines.append(f"TO: {_clean(p['to'])}")
        elif p["change"] == "DELETE":
            lines.append(f"FROM: {_clean(p['from'])}")
        else:
            die(f"Unsupported change type in proposer: {p['change']}")

        lines.append("")
        n += 1

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_propose_changes_ai")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--rr-occurrence", type=int, default=1, help="1-indexed Roles and Responsibilities occurrence (default: 1)")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path
    pipe = app / "resume_refs" / "resume_pipeline"
    pipe.mkdir(parents=True, exist_ok=True)

    # Stage inputs (must exist)
    job_json = pipe / "job.json"
    selection_json = pipe / "selection.json"
    emphasis_json = pipe / "emphasis.json"
    jd_raw = app / "jd" / "jd-raw.txt"

    if not job_json.exists():
        die(f"Missing Stage 1 output: {job_json}\nRun: resume load-job --app \"{app}\" --write-debug")
    if not selection_json.exists():
        die(f"Missing Stage 2 output: {selection_json}\nRun: resume select-template --app \"{app}\" --write")
    if not emphasis_json.exists():
        die(f"Missing Stage 3 output: {emphasis_json}\nRun: resume emphasis-tags --app \"{app}\" --write")
    if not jd_raw.exists():
        die(f"Missing JD file: {jd_raw}")

    selection = load_json(selection_json)
    selected_slug = selection["selected"]["template_slug"]

    emphasis = load_json(emphasis_json)
    tags = emphasis.get("active_tags", [])
    if not isinstance(tags, list):
        tags = []

    jd_text = read_text(jd_raw)

    out_path = pipe / "proposed-changes.md"
    if out_path.exists() and not args.force:
        die(f"Refusing to overwrite existing proposed-changes.md (use --force): {out_path}")

    proposals = _stub_generate_real_proposals(
        family=resolved.family,
        selected_slug=selected_slug,
        emphasis_tags=tags,
        jd_text=jd_text,
        rr_occurrence=args.rr_occurrence,
    )

    # hard ban placeholder tokens
    blob = json.dumps(proposals)
    if "[PROPOSED:" in blob or "[PLACEHOLDER:" in blob:
        die("Internal error: proposer generated placeholder text")

    _write_proposed_changes_md(out_path, resolved, selected_slug, proposals)
    print(str(out_path))


if __name__ == "__main__":
    main()
