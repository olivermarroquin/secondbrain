from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

class RFPathError(Exception):
    pass

@dataclass(frozen=True)
class RFResolvedApp:
    app_path: Path
    jobs_root: Path
    family: str
    company: str
    role_slug: str

    templates_root: Path
    outputs_root: Path

def _die(msg: str) -> None:
    raise RFPathError(msg)

def resolve_app(app: str | Path, root: str | Path = "~/secondbrain") -> RFResolvedApp:
    """
    Resolve and validate a Resume Factory APP path.

    Expected APP format:
      <root>/01_projects/jobs/<family>/<company>/<YYYY-MM-DD_role-slug>

    Returns:
      RFResolvedApp with templates_root and outputs_root resolved.
    """
    rootp = Path(root).expanduser().resolve()
    jobs_root = (rootp / "01_projects" / "jobs").resolve()

    app_path = Path(app).expanduser().resolve()
    if not app_path.exists():
        _die(f"APP does not exist: {app_path}")
    if not app_path.is_dir():
        _die(f"APP is not a directory: {app_path}")

    # Validate that APP is under jobs_root
    try:
        rel = app_path.relative_to(jobs_root)
    except ValueError:
        _die(f"APP is not under jobs root: {jobs_root}\nAPP: {app_path}")

    # rel should be: family/company/role_slug
    parts = rel.parts
    if len(parts) != 3:
        _die(
            "APP path must be exactly 3 levels under jobs root:\n"
            f"  jobs/<family>/<company>/<role_slug>\n"
            f"Got: {rel}"
        )

    family, company, role_slug = parts

    # Resolve templates root for this family
    templates_root = (rootp / "03_assets" / "templates" / "resumes" / family).resolve()
    if not templates_root.exists():
        _die(f"No templates directory for family '{family}': {templates_root}")

    # Resolve outputs root base for this job
    outputs_root = (rootp / "05_outputs" / "resumes" / family / company / role_slug).resolve()

    return RFResolvedApp(
        app_path=app_path,
        jobs_root=jobs_root,
        family=family,
        company=company,
        role_slug=role_slug,
        templates_root=templates_root,
        outputs_root=outputs_root,
    )

def list_templates(resolved: RFResolvedApp) -> list[Path]:
    """
    List template directories under templates_root.
    A template directory must contain resume-master.docx.
    """
    troot = resolved.templates_root
    if not troot.exists():
        _die(f"Templates root missing: {troot}")

    dirs = [p for p in sorted(troot.iterdir()) if p.is_dir()]
    good = []
    for d in dirs:
        if (d / "resume-master.docx").exists():
            good.append(d)
    if not good:
        _die(f"No templates found under: {troot} (expected */resume-master.docx)")
    return good
