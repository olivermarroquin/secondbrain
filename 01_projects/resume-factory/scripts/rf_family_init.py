#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def norm_family(s: str) -> str:
    s = s.strip()
    if not s:
        die("family is required")
    # conservative: folder-safe
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
    lower = s.lower()
    if any(ch not in allowed for ch in lower):
        die("family must be lowercase and folder-safe: [a-z0-9_]")
    return lower

DEFAULT_TEMPLATE_DIRS = [
    ("01_template_1", "01_template_1"),
    ("02_template_2", "02_template_2"),
    ("03_template_3", "03_template_3"),
    ("04_template_4", "04_template_4"),
]

def load_json(p: Path) -> dict:
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8", errors="replace"))

def atomic_write_json(p: Path, obj: dict) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)

def ensure_aliases_family(root: Path, family: str, force: bool = False) -> None:
    aliases_path = root / "01_projects" / "resume-factory" / "schemas" / "section-aliases.json"
    aliases_path.parent.mkdir(parents=True, exist_ok=True)

    doc = load_json(aliases_path)
    if not doc:
        doc = {"schema": "rf_section_aliases_v1", "families": {}}
    if "families" not in doc or not isinstance(doc["families"], dict):
        die(f"Invalid aliases schema (missing families dict): {aliases_path}")

    fams = doc["families"]
    if family in fams and not force:
        print(f"aliases: family already exists (no change): {family}")
        return

    # Minimal placeholder mapping. User edits later per-family.
    fams[family] = {
        "__MAJOR_HEADINGS__": [
            "SUMMARY:",
            "SKILLS:",
            "EXPERIENCE:",
            "EDUCATION:"
        ],
        "__SUBSECTIONS__": {
            "ROLES_AND_RESPONSIBILITIES": ["Roles and Responsibilities:"]
        },
        "SUMMARY": ["SUMMARY:", "PROFESSIONAL SUMMARY:", "SUMMARY"],
        "CORE COMPETENCIES": ["SKILLS:", "TECHNICAL SKILL:", "TECHNICAL SKILLS:", "CORE COMPETENCIES:"],
        "PROJECT EXPERIENCE": ["EXPERIENCE:", "PROFESSIONAL EXPERIENCE:", "PROJECT EXPERIENCE:"]
    }

    atomic_write_json(aliases_path, doc)
    print(f"aliases: ensured family entry: {family}")

def template_dir_for(root: Path, family: str) -> Path:
    return root / "03_assets" / "templates" / "resumes" / family

def detect_template_folders(family_dir: Path) -> list[Path]:
    if not family_dir.exists():
        return []
    return sorted([p for p in family_dir.iterdir() if p.is_dir() and p.name[:2].isdigit()])

def copy_tree(src: Path, dst: Path, force: bool) -> None:
    if dst.exists():
        if not force:
            die(f"Destination exists (use --force): {dst}")
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_family_init")
    ap.add_argument("--family", required=True, help="Job family slug (lowercase a-z0-9_)")
    ap.add_argument("--from-family", default="", help="Optional: clone templates from existing family")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Allow overwriting existing family templates entry")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    family = norm_family(args.family)
    from_family = norm_family(args.from_family) if args.from_family.strip() else ""

    fam_dir = template_dir_for(root, family)
    src_dir = template_dir_for(root, from_family) if from_family else None

    # Templates
    if from_family:
        if not src_dir.exists():
            die(f"--from-family templates not found: {src_dir}")
        if fam_dir.exists() and not args.force:
            die(f"family templates dir already exists (use --force): {fam_dir}")
        copy_tree(src_dir, fam_dir, force=args.force)
        print(f"templates: cloned {from_family} -> {family}: {fam_dir}")
    else:
        fam_dir.mkdir(parents=True, exist_ok=True)
        existing = detect_template_folders(fam_dir)
        if existing and not args.force:
            die(f"family templates already initialized (use --force): {fam_dir}")

        # create 4 placeholder folders (you replace names/files later)
        for slug, folder in DEFAULT_TEMPLATE_DIRS:
            tdir = fam_dir / folder
            if tdir.exists() and args.force:
                shutil.rmtree(tdir)
            tdir.mkdir(parents=True, exist_ok=True)
            readme = tdir / "README.md"
            if not readme.exists():
                readme.write_text(
                    f"# {family}/{folder}\n\n"
                    "Place these files here:\n"
                    "- resume-master.docx\n"
                    "- signals.json\n",
                    encoding="utf-8"
                )
        print(f"templates: scaffolded 4 placeholder template dirs: {fam_dir}")

    # Aliases schema entry (non-destructive)
    ensure_aliases_family(root, family, force=False)

if __name__ == "__main__":
    main()
