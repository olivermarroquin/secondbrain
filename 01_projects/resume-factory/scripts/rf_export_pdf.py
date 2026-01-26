#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing required file: {p}")
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_export_pdf")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Overwrite resume.pdf if it exists")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    app = Path(args.app).expanduser().resolve()

    # derive output paths from build meta (source of truth)
    meta_path = root / "05_outputs" / "resumes"
    # meta location is deterministic in your pipeline; read build meta from job pointer
    job_ptr = app / "resume_refs" / "resume_pipeline" / "job.json"
    job = load_json(job_ptr)
    family = job["app"]["family"]
    company = job["app"]["company"]
    role_slug = job["app"]["role_slug"]

    out_base = root / "05_outputs" / "resumes" / family / company / role_slug
    docx_path = out_base / "resume" / "resume.docx"
    pdf_path = out_base / "resume" / "resume.pdf"

    if not docx_path.exists():
        die(f"Missing DOCX to convert: {docx_path}\nRun: resume build-docx --app \"{app}\"")

    if pdf_path.exists() and not args.force:
        die(f"PDF already exists (use --force): {pdf_path}")

    # find libreoffice/soffice
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        die("LibreOffice not found (need 'soffice' in PATH).\nInstall: brew install --cask libreoffice\nThen re-run export-pdf.")

    # LibreOffice writes output into target directory with same basename
    outdir = pdf_path.parent
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--convert-to", "pdf",
        "--outdir", str(outdir),
        str(docx_path),
    ]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        die(f"Failed to run LibreOffice: {e}")

    if r.returncode != 0:
        die(f"LibreOffice conversion failed:\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}")

    produced = outdir / (docx_path.stem + ".pdf")
    if not produced.exists():
        die(f"Conversion did not produce expected file: {produced}")

    if produced != pdf_path:
        # normalize name
        if pdf_path.exists():
            pdf_path.unlink()
        produced.replace(pdf_path)

    print(str(pdf_path))

if __name__ == "__main__":
    main()
