# 01_projects/resume-factory/scripts/rf_ideal_profile_schema.py
from __future__ import annotations

from typing import Any, Dict, Tuple

def _die(msg: str) -> Tuple[bool, str]:
    return False, msg

def validate_ideal_profile(payload: Any) -> Tuple[bool, str]:
    """
    Validates ideal-profile payload shape (not correctness).

    Contract:
    {
      "ideal_profile": {
        "must_haves": [str,...],
        "nice_to_haves": [str,...],
        "domain_context": [str,...],
        "core_responsibilities": [str,...],
        "signals_of_seniority": [str,...],
        "risks_red_flags": [str,...]
      },
      "notes": str (optional)
    }
    """
    if not isinstance(payload, dict):
        return _die("payload must be an object")

    ip = payload.get("ideal_profile")
    if not isinstance(ip, dict):
        return _die("ideal_profile must be an object")

    def _req_list(name: str, min_items: int = 1) -> Tuple[bool, str]:
        v = ip.get(name)
        if not isinstance(v, list) or len(v) < min_items:
            return _die(f"ideal_profile.{name} must be a list with >= {min_items} items")
        if not all(isinstance(x, str) and x.strip() for x in v):
            return _die(f"ideal_profile.{name} must be a list of non-empty strings")
        return True, "ok"

    # Keep minimums sane but not restrictive
    ok, msg = _req_list("must_haves", 3)
    if not ok: return ok, msg
    ok, msg = _req_list("nice_to_haves", 2)
    if not ok: return ok, msg
    ok, msg = _req_list("domain_context", 1)
    if not ok: return ok, msg
    ok, msg = _req_list("core_responsibilities", 3)
    if not ok: return ok, msg
    ok, msg = _req_list("signals_of_seniority", 2)
    if not ok: return ok, msg
    ok, msg = _req_list("risks_red_flags", 1)
    if not ok: return ok, msg

    notes = payload.get("notes", None)
    if notes is not None and not isinstance(notes, str):
        return _die("notes must be a string if present")

    return True, "ok"

def json_schema_for_structured_outputs() -> Dict[str, Any]:
    # Optional future use: OpenAI structured outputs.
    return {
        "name": "resume_ideal_profile",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["ideal_profile"],
            "properties": {
                "ideal_profile": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "must_haves",
                        "nice_to_haves",
                        "domain_context",
                        "core_responsibilities",
                        "signals_of_seniority",
                        "risks_red_flags",
                    ],
                    "properties": {
                        "must_haves": {"type": "array", "minItems": 3, "items": {"type": "string"}},
                        "nice_to_haves": {"type": "array", "minItems": 2, "items": {"type": "string"}},
                        "domain_context": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                        "core_responsibilities": {"type": "array", "minItems": 3, "items": {"type": "string"}},
                        "signals_of_seniority": {"type": "array", "minItems": 2, "items": {"type": "string"}},
                        "risks_red_flags": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                    },
                },
                "notes": {"type": "string"},
            },
        },
        "strict": True,
    }
