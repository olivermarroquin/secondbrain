import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Optional
from datetime import date

def die(msg, code=2):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def valid_snake(s): return re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", s) is not None
def valid_kebab(s): return re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s) is not None
def valid_date(s): return re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) is not None

@dataclass(frozen=True)
class JobIntake:
    family: str
    company_slug: str
    date_found: str
    role_slug: str
    role_title: str
    source_url: str
    location: str = "unknown"
    seniority: str = "unknown"
    employment_type: str = "unknown"
    priority: str = "unknown"

def today_yyyy_mm_dd() -> str:
    return date.today().isoformat()

def build_app_dir(root: pathlib.Path, ji: JobIntake) -> pathlib.Path:
    return root / "01_projects" / "jobs" / ji.family / ji.company_slug / f"{ji.date_found}_{ji.role_slug}"


def find_existing_by_url(root: pathlib.Path, family: str, url: str) -> Optional[pathlib.Path]:
    """
    Return the app_dir of an existing job whose tracking/job-meta.json has source==url
    or whose jd/job-post-url.txt matches url. Scans only within the same family.
    """
    base = root / "01_projects" / "jobs" / family
    if not base.exists():
        return None

    # First: check job-meta.json source fields
    for jm in base.glob("**/tracking/job-meta.json"):
        try:
            d = json.loads(jm.read_text())
            if (d.get("source") or "").strip() == url:
                return jm.parent.parent
        except Exception:
            continue

    # Second: check mirror file
    for up in base.glob("**/jd/job-post-url.txt"):
        try:
            if up.read_text().strip() == url:
                return up.parent.parent
        except Exception:
            continue

    return None


def write_job_folder(root: pathlib.Path, ji: JobIntake, jd_text: str, dry_run: bool, force: bool):
    # basic validation
    if not valid_snake(ji.company_slug):
        die(f"company_slug must be snake_case: {ji.company_slug}")
    if not valid_kebab(ji.role_slug):
        die(f"role_slug must be kebab-case: {ji.role_slug}")
    if not valid_date(ji.date_found):
        die(f"date_found must be YYYY-MM-DD: {ji.date_found}")
    if not ji.source_url.startswith(("http://", "https://")):
        die("source_url must be http(s)")

    app_dir = build_app_dir(root, ji)
    jd_dir = app_dir / "jd"
    tracking_dir = app_dir / "tracking"

    jm_path = tracking_dir / "job-meta.json"
    ar_path = tracking_dir / "application-record.json"
    sh_path = tracking_dir / "status-history.md"
    jd_raw  = jd_dir / "jd-raw.txt"
    jd_url  = jd_dir / "job-post-url.txt"


    # duplicate-url guard (family-wide)
    if not force:
        existing = find_existing_by_url(root, ji.family, ji.source_url)
        if existing is not None and existing != app_dir:
            return ("SKIPPED", existing, "duplicate_url")

    # idempotency: refuse overwrite unless force
    for p in [jm_path, ar_path, sh_path]:
        if p.exists() and not force:
            return ("SKIPPED", app_dir, f"exists: {p.name}")

    if dry_run:
        return ("DRYRUN", app_dir, "would create/write")

    # create dirs (mirror job-intake-init)
    for p in [jd_dir, tracking_dir, app_dir/"resume_refs", app_dir/"notes"]:
        p.mkdir(parents=True, exist_ok=True)

    app_id = f"{ji.company_slug}_{ji.date_found}_{ji.role_slug}"

    job_meta = {
        "company": ji.company_slug,
        "role_family": ji.family,
        "role_title": ji.role_title,
        "seniority": ji.seniority,
        "location": ji.location,
        "employment_type": ji.employment_type,
        "source": ji.source_url,
        "date_found": ji.date_found,
        "date_applied": None,
        "status": "not_applied",
        "priority": ji.priority,
    }

    app_record = {
        "application_id": app_id,
        "current_status": "not_applied",
        "status_history": [],
        "resume_used": None,
        "cover_letter_used": None,
        "notes": "",
    }

    status_md = f"""# Status History

## {ji.date_found}
- Job identified
- JD captured (pending paste)
- Application not yet submitted
"""

    jm_path.write_text(json.dumps(job_meta, indent=2) + "\n")
    ar_path.write_text(json.dumps(app_record, indent=2) + "\n")
    sh_path.write_text(status_md)

    jd_url.write_text(ji.source_url + "\n")
    # always write JD
    jd_raw.write_text(jd_text.rstrip() + "\n")

    return ("CREATED", app_dir, "ok")
