# AI Materializer Contract v1 (Resume Factory)

## Purpose
Generate `patches.json` from human approvals. This is the ONLY place where “intelligence” writes final text.

## Inputs (read-only)
Under: APP/resume_refs/resume_pipeline/

Required:
- proposed-changes.md
- approvals.json
- job.json
- selection.json
Optional:
- emphasis.json

## Output (write)
- patches.json  (schema: rf_patches_v1)

## Hard rules (must)
1) Only emit patches for `approved_change_numbers` in approvals.json.
2) MUST NOT emit placeholder text:
   - No `[PROPOSED:` or `[PLACEHOLDER:`
3) MUST preserve numbering:
   - patches[].num must match approved numbers
4) MUST NOT add extra approvals or change them.
5) Must be deterministic given the same inputs (no randomness).
6) Content must be realistic and consistent with the selected template and JD.

## Patch ops allowed (v1)
- ADD
  - Provide `to_text` (string), optionally `section` and optionally subsection anchors:
    - subsection: "ROLES_AND_RESPONSIBILITIES"
    - subsection_occurrence: 1/2/3...
- REPLACE_SECTION
  - Provide `to_paragraphs` (array of strings) OR `to_text` with newline separators
- DELETE
  - Provide `from_text` (string)

## Failure behavior
If anything is missing or contradictory, fail fast with a clear error and do not write patches.json.
