# NEXT (Project)

## Scope
- Project: resume-factory
- Path: 01_projects/resume-factory
- Applies to: This project only

## Focus
Focus: Automate end-to-end resume tailoring, tracking, and interview prep from job descriptions

## Task #0 — State correction (always allowed)
- If this file does not accurately represent the next actions, update it before doing any other work.
- Updating NEXT.md does not require a prior commit.

## Execution Rules
- Tasks are executed top-down.
- Do not skip tasks unless explicitly marked optional.
- If a task becomes invalid, mark it as [obsolete] and explain why.
- New tasks are appended (do not insert above in-progress work).

## Next Actions Queue (this will be empty later for AI to be able to use it)
1) Golden run Job #1: run intake → verify → resume-select/preview → suggest edits → approve edits → generate resume.docx
2) Golden run Job #1: run jobs-apply-batch (dry-run → real) → apply → prune if needed → jobs-mark-applied-last (dry-run → apply/commit/push)
3) Close session correctly (git clean, session-close)