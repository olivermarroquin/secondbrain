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
from rf_paths import resolve_app, list_templates, RFPathError  # type: ignore

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
    """
    Counts simple substring hits per keyword (normalized).
    Deterministic and explainable. No ML.
    """
    t = norm(text)
    hits: dict[str, int] = {}
    for kw in keywords:
        k = norm(kw)
        if not k:
            continue
        # count non-overlapping occurrences
        hits[kw] = len(re.findall(re.escape(k), t))
    return hits

def score_template(jd_text: str, signals: dict) -> dict:
    pref = signals.get("preferred_keywords", []) or []
    neut = signals.get("neutral_keywords", []) or []
    anti = signals.get("anti_signals", []) or []

    pref_hits = count_hits(jd_text, pref)
    neut_hits = count_hits(jd_text, neut)
    anti_hits = count_hits(jd_text, anti)

    # Weights: keep it boring and stable.
    # preferred: +10 each hit
    # neutral:   +2 each hit
    # anti:      -20 each hit (anti means the template is likely wrong)
    pref_score = sum(v * 10 for v in pref_hits.values())
    neut_score = sum(v * 2 for v in neut_hits.values())
    anti_score = sum(v * 20 for v in anti_hits.values())

    total = pref_score + neut_score - anti_score

    return {
        "score_total": total,
        "score_components": {
            "preferred": pref_score,
            "neutral": neut_score,
            "anti_penalty": anti_score,
        },
        "hits": {
            "preferred": {k: v for k, v in pref_hits.items() if v},
            "neutral": {k: v for k, v in neut_hits.items() if v},
            "anti": {k: v for k, v in anti_hits.items() if v},
        }
    }

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_select_template")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--write", action="store_true", help="Write selection.json to resume_refs/resume_pipeline/")
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

    templates = list_templates(resolved)

    scored = []
    for tdir in templates:
        sig_path = tdir / "signals.json"
        if not sig_path.exists():
            die(f"Template missing signals.json (required): {sig_path}")

        signals = read_json(sig_path)
        if signals.get("schema") != "rf_signals_v2":
            die(f"signals.json schema mismatch (expected rf_signals_v2): {sig_path}")

        s = score_template(jd_text, signals)
        scored.append({
            "template_dir": str(tdir),
            "template_slug": signals.get("template_slug"),
            "template_id": signals.get("template_id"),
            "signals_path": str(sig_path),
            **s
        })

    scored.sort(key=lambda x: (x["score_total"], x.get("template_id") or ""), reverse=True)
    best = scored[0]

    out = {
        "schema": "rf_selection_v1",
        "selected_at_utc": datetime.now(timezone.utc).isoformat(),
        "app": {
            "app_path": str(resolved.app_path),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },
        "selected": {
            "template_id": best.get("template_id"),
            "template_slug": best.get("template_slug"),
            "template_dir": best["template_dir"],
            "signals_path": best["signals_path"],
            "score_total": best["score_total"],
            "score_components": best["score_components"],
            "hits": best["hits"],
        },
        "candidates": scored[:4],
    }

    if args.write:
        out_dir = app / "resume_refs" / "resume_pipeline"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "selection.json"
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(str(out_path))
    else:
        print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
