# Resume Factory — Context

Checkpoint system overview:
See ../../07_system/checkpoints/resume-factory/README.md

Authoritative checkpoint pointer:
- ../../07_system/checkpoints/resume-factory/LATEST.md

Read order for system context:
1) This CONTEXT.md
2) ../../07_system/checkpoints/resume-factory/LATEST.md
3) ../../07_system/checkpoints/resume-factory/CURRENT.md

Operator helpers live in: ../../01_projects/resume-factory/scripts/ (rf-context, rf-checkpoint, rf-idea)

Rules:
- Make small, testable changes.
- Add verification steps.
- No redesign unless explicitly requested.
- Preserve existing CLI UX unless improving determinism.

This file is a pointer and ruleset, not a source of system truth or history.
