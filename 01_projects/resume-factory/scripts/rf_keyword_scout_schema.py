from __future__ import annotations

from typing import Any, Dict, List, Tuple

def _die(msg: str) -> Tuple[bool, str]:
    return False, msg

def validate_keyword_scout(payload: Any) -> Tuple[bool, str]:
    """
    Validates keyword-scout.json shape (not "correctness").
    Contract:
      {
        "keywords_tools_ranked": [ {"term": str, "type": "keyword"|"tool", "why": str, "evidence": [str,...]}, ... ],
        "implied_responsibilities_flows": [ {"flow": str, "why": str, "evidence": [str,...]}, ... ],
        "notes": str (optional)
      }
    """
    if not isinstance(payload, dict):
        return _die("payload must be an object")

    k = payload.get("keywords_tools_ranked")
    f = payload.get("implied_responsibilities_flows")
    if not isinstance(k, list) or not k:
        return _die("keywords_tools_ranked must be a non-empty list")
    if not isinstance(f, list) or not f:
        return _die("implied_responsibilities_flows must be a non-empty list")

    for i, row in enumerate(k, start=1):
        if not isinstance(row, dict):
            return _die(f"keywords_tools_ranked[{i}] must be an object")
        term = row.get("term")
        typ = row.get("type")
        why = row.get("why")
        ev = row.get("evidence", [])
        if not isinstance(term, str) or not term.strip():
            return _die(f"keywords_tools_ranked[{i}].term must be a non-empty string")
        if typ not in ("keyword", "tool"):
            return _die(f"keywords_tools_ranked[{i}].type must be 'keyword' or 'tool'")
        if not isinstance(why, str) or not why.strip():
            return _die(f"keywords_tools_ranked[{i}].why must be a non-empty string")
        if not isinstance(ev, list) or not ev or not all(isinstance(x, str) and x.strip() for x in ev):
            return _die(f"keywords_tools_ranked[{i}].evidence must be a non-empty list of strings")

    for i, row in enumerate(f, start=1):
        if not isinstance(row, dict):
            return _die(f"implied_responsibilities_flows[{i}] must be an object")
        flow = row.get("flow")
        why = row.get("why")
        ev = row.get("evidence", [])
        if not isinstance(flow, str) or not flow.strip():
            return _die(f"implied_responsibilities_flows[{i}].flow must be a non-empty string")
        if not isinstance(why, str) or not why.strip():
            return _die(f"implied_responsibilities_flows[{i}].why must be a non-empty string")
        if not isinstance(ev, list) or not ev or not all(isinstance(x, str) and x.strip() for x in ev):
            return _die(f"implied_responsibilities_flows[{i}].evidence must be a non-empty list of strings")

    notes = payload.get("notes", None)
    if notes is not None and not isinstance(notes, str):
        return _die("notes must be a string if present")

    return True, "ok"

def json_schema_for_structured_outputs() -> Dict[str, Any]:
    # Optional future use: OpenAI structured outputs.
    return {
        "name": "resume_keyword_scout",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["keywords_tools_ranked", "implied_responsibilities_flows"],
            "properties": {
                "keywords_tools_ranked": {
                    "type": "array",
                    "minItems": 10,
                    "maxItems": 25,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["term", "type", "why", "evidence"],
                        "properties": {
                            "term": {"type": "string"},
                            "type": {"type": "string", "enum": ["keyword", "tool"]},
                            "why": {"type": "string"},
                            "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                        },
                    },
                },
                "implied_responsibilities_flows": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 12,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["flow", "why", "evidence"],
                        "properties": {
                            "flow": {"type": "string"},
                            "why": {"type": "string"},
                            "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                        },
                    },
                },
                "notes": {"type": "string"},
            },
        },
        "strict": True,
    }
