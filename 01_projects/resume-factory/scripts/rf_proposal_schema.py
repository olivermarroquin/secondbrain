from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

ALLOWED_SECTIONS = {"SUMMARY", "SKILLS", "EXPERIENCE"}
ALLOWED_OPS = {"REPLACE_LINE", "REPLACE_PHRASE"}

@dataclass(frozen=True)
class Proposal:
    section: str
    op: str
    before: List[str]
    after: List[str]
    rationale: str

def _die(msg: str) -> Tuple[bool, str]:
    return False, msg

def validate_proposals(proposals: Any) -> Tuple[bool, str]:
    """
    Deterministic schema gate before writing edit-proposals.json.

    Accepts:
      proposals: list[dict] where each dict has:
        - section: SUMMARY|SKILLS|EXPERIENCE
        - op: REPLACE_LINE|REPLACE_PHRASE
        - before: [str]  (non-empty strings)
        - after:  [str]  (non-empty strings)
        - rationale: str (non-empty)
    """
    if not isinstance(proposals, list):
        return _die("proposals must be a list")

    for i, p in enumerate(proposals, start=1):
        if not isinstance(p, dict):
            return _die(f"proposal #{i}: must be an object")

        section = p.get("section")
        op = p.get("op")
        before = p.get("before")
        after = p.get("after")
        rationale = p.get("rationale")

        if section not in ALLOWED_SECTIONS:
            return _die(f"proposal #{i}: invalid section={section!r}")
        if op not in ALLOWED_OPS:
            return _die(f"proposal #{i}: invalid op={op!r}")

        if not isinstance(before, list) or not before or not all(isinstance(x, str) and x.strip() for x in before):
            return _die(f"proposal #{i}: before must be a non-empty list of non-empty strings")
        if not isinstance(after, list) or not after or not all(isinstance(x, str) and x.strip() for x in after):
            return _die(f"proposal #{i}: after must be a non-empty list of non-empty strings")
        if not isinstance(rationale, str) or not rationale.strip():
            return _die(f"proposal #{i}: rationale must be a non-empty string")

        # Op-specific constraints:
        if op == "REPLACE_LINE":
            if len(before) != 1 or len(after) != 1:
                return _die(f"proposal #{i}: REPLACE_LINE requires before/after length of 1")
        # REPLACE_PHRASE can still be 1->1 (we keep it strict/simple)
        if op == "REPLACE_PHRASE":
            if len(before) != 1 or len(after) != 1:
                return _die(f"proposal #{i}: REPLACE_PHRASE requires before/after length of 1")

    return True, "ok"

def json_schema_for_structured_outputs() -> Dict[str, Any]:
    """
    JSON Schema used for OpenAI Structured Outputs.
    Keep this in sync with validate_proposals().
    """
    return {
        "name": "resume_edit_proposals",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["proposals"],
            "properties": {
                "proposals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["section", "op", "before", "after", "rationale"],
                        "properties": {
                            "section": {"type": "string", "enum": sorted(ALLOWED_SECTIONS)},
                            "op": {"type": "string", "enum": sorted(ALLOWED_OPS)},
                            "before": {"type": "array", "minItems": 1, "maxItems": 1, "items": {"type": "string"}},
                            "after": {"type": "array", "minItems": 1, "maxItems": 1, "items": {"type": "string"}},
                            "rationale": {"type": "string"},
                        },
                    },
                }
            },
        },
        "strict": True,
    }
