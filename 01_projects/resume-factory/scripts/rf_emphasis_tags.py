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
    return p.read_text(encoding="utf-8", errors="replace")

def read_json(p: Path):
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def count_hits(text: str, keywords: list[str]) -> dict[str, int]:
    t = norm(text)
    hits: dict[str, int] = {}
    for kw in keywords:
        k = norm(kw)
        if not k:
            continue
        hits[kw] = len(re.findall(re.escape(k), t))
    return hits

# Locked categories (extend keyword lists carefully; keep stable)
TAGS: dict[str, list[str]] = {
    "api": [
        "api", "rest", "restful", "graphql", "postman", "rest assured", "soap",
        "http", "endpoint", "swagger", "openapi"
    ],
    "perf": [
        "performance", "load testing", "stress testing", "jmeter", "gatling",
        "k6", "latency", "throughput"
    ],
    "cloud": [
        "aws", "azure", "gcp", "cloud", "kubernetes", "docker", "ecs", "eks",
        "lambda", "terraform", "helm"
    ],
    "etl": [
        "etl", "data pipeline", "data pipelines", "data warehouse", "warehouse",
        "spark", "airflow", "dbt", "snowflake", "redshift", "bigquery"
    ],
    "mobile": [
        "mobile", "android", "ios", "appium", "xcode", "espresso", "xcuitest"
    ],
    "ai_ml": [
        "machine learning", "ml", "ai", "model", "llm", "genai", "prompt",
        "computer vision", "nlp"
    ],
}

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_emphasis_tags")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--write", action="store_true", help="Write emphasis.json to resume_refs/resume_pipeline/")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path
    job_json = app / "resume_refs" / "resume_pipeline" / "job.json"
    if not job_json.exists():
        die(f"Missing Stage 1 output: {job_json}\nRun: resume load-job --app \"$APP\" --write-debug")

    job = read_json(job_json)
    jd_text = job.get("jd_raw", "")
    if not jd_text or not isinstance(jd_text, str):
        die("job.json missing jd_raw")

    tag_results = {}
    for tag, kws in TAGS.items():
        hits = count_hits(jd_text, kws)
        present = {k: v for k, v in hits.items() if v}
        tag_results[tag] = {
            "hit_count": sum(present.values()),
            "hits": present,
        }

    # sorted tags by hit_count desc, then name
    ordered = sorted(tag_results.items(), key=lambda kv: (kv[1]["hit_count"], kv[0]), reverse=True)
    active = [name for name, meta in ordered if meta["hit_count"] > 0]

    out = {
        "schema": "rf_emphasis_v1",
        "tagged_at_utc": datetime.now(timezone.utc).isoformat(),
        "app": {
            "app_path": str(resolved.app_path),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },
        "active_tags": active,
        "tags": tag_results,
    }

    if args.write:
        out_dir = app / "resume_refs" / "resume_pipeline"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "emphasis.json"
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(str(out_path))
    else:
        print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
