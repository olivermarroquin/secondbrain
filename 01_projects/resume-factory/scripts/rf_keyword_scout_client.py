from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Optional

from openai import OpenAI
from openai import RateLimitError, AuthenticationError

def _keyword_scout_json_schema() -> dict:
    return {
        "name": "keyword_scout",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["keywords_tools_ranked", "implied_responsibilities_flows", "notes"],
            "properties": {
                "keywords_tools_ranked": {
                    "type": "array",
                    "minItems": 10,
                    "maxItems": 20,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["term", "type", "why", "evidence"],
                        "properties": {
                            "term": {"type": "string"},
                            "type": {"type": "string", "enum": ["keyword", "tool"]},
                            "why": {"type": "string"},
                            "evidence": {
                                "type": "array",
                                "minItems": 1,
                                "maxItems": 3,
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
                "implied_responsibilities_flows": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 7,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["flow", "why", "evidence"],
                        "properties": {
                            "flow": {"type": "string"},
                            "why": {"type": "string"},
                            "evidence": {
                                "type": "array",
                                "minItems": 1,
                                "maxItems": 3,
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
                "notes": {"type": "string"},
            },
        },
        "strict": True,
    }


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    return v if (v is not None and v != "") else default

def _require(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"missing required env var: {name}")
    return v

def keyword_scout_openai(
    *,
    jd_raw: str,
    baseline_text: str = "",
    baseline_covered_terms: Optional[list] = None,
    model: Optional[str] = None,
    timeout_s: int = 90,
    extra_instructions: str = "",
) -> Dict[str, Any]:
    _require("OPENAI_API_KEY")
    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_KEYWORD_SCOUT_MODEL", "gpt-4o-mini")

    system_prompt = """You are Resume Factory - Keyword Scout.

OUTPUT RULES:
- You will be given BASELINE RESUME CONTEXT (what is already covered in the selected template).
- Prefer JD keywords/tools that are NOT already covered in the baseline.
- You MAY include baseline-covered terms if they are truly critical for the role, but don't waste slots on obvious basics.

- Return STRICT JSON ONLY (no markdown, no commentary).
- Choose the BEST 10–20 keywords/tools that are PRESENT IN THE JOB DESCRIPTION.
- Prefer SPECIFIC tool names as written in the JD (e.g., 'JMeter', 'App Scan', 'Twistlock') over generic categories like 'Load Testing' or 'Security Testing'.
- The "type" field MUST be exactly either "keyword" or "tool".
- Never use values like "protocol", "framework", "language", "technology", or any other label.
- If the term is a tool name (e.g., JMeter, Jenkins, Twistlock), use "tool".
- Everything else must use "keyword".

- Prefer RARE / HIGH-SIGNAL tokens over generic QA nouns. High-signal = product/tool names, protocols (SFTP/HTTPs/RPC/sockets), accessibility tooling, security scanners, exact framework names, '12 factor applications'.
- Generic terms (e.g., 'test plans', 'functional testing', 'integration testing') are allowed ONLY if they are unusually emphasized in the JD; otherwise they should lose to specific tools/protocols.
- You are unconstrained in judgment: pick what matters most for this role.
- For every item, include evidence: short exact phrases copied from the JD (1–3 snippets).

JSON CONTRACT:
{
  "keywords_tools_ranked": [
    {"term": "<keyword or tool>", "type": "keyword|tool", "why": "<1-2 sentences>", "evidence": ["<exact JD snippet>", "..."]}
  ],
  "implied_responsibilities_flows": [
    {"flow": "<responsibility/flow>", "why": "<1-2 sentences>", "evidence": ["<exact JD snippet>", "..."]}
  ],
  "notes": "<optional>"
}
"""

    baseline_block = (baseline_text or "").strip()
    if baseline_covered_terms is None:
        baseline_covered_terms = []
    covered_terms = ", ".join([str(x) for x in baseline_covered_terms[:120]]) if baseline_covered_terms else "(none)"

    user_prompt = f"""JOB DESCRIPTION (source of truth):
{jd_raw}

BASELINE RESUME CONTEXT (already covered in the selected template):
{baseline_block}

BASELINE COVERED TERMS (hint list; don't over-index on them):
{covered_terms}

TASK:
Return the JSON contract. Pick the best 10–20 keywords/tools and 3–7 implied responsibilities/flows.

EXTRA INSTRUCTIONS:
{extra_instructions}"""
    # If the model returns almost-JSON with a tiny syntax slip, do ONE deterministic repair pass.
    # This does not change content; it only fixes JSON validity.
    def _repair_json_once(bad_text: str) -> str:
        repair_system = """You are a JSON repair bot.
RULES:
- Output STRICT JSON ONLY.
- Do NOT add new items or remove items.
- Do NOT change meaning.
- Only fix JSON syntax/escaping/commas/quotes to make it valid JSON that matches the contract.
"""
        repair_user = f"""JSON_REPAIR_TASK:
Fix this into valid JSON (same structure/content; syntax repair only):

{bad_text}
"""
        r = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": repair_system.strip()},
                {"role": "user", "content": repair_user.strip()},
            ],
        )
        out = ""
        for o in r.output:
            for c in o.content:
                if c.type == "output_text":
                    out += c.text
        out = (out or "").strip()
        m = re.match(r"^```(?:json)?\s*(.*?)\s*```\s*$", out, flags=re.DOTALL | re.IGNORECASE)
        if m:
            out = m.group(1).strip()
        return out

    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
        )
    except AuthenticationError as e:
        raise RuntimeError("OpenAI auth failed (invalid API key).") from e
    except RateLimitError as e:
        msg = str(e)
        if "insufficient_quota" in msg or "check your plan and billing details" in msg:
            raise RuntimeError("OpenAI quota/billing blocked this request (insufficient_quota).") from e
        raise

    text = ""
    for out in resp.output:
        for c in out.content:
            if c.type == "output_text":
                text += c.text
    t = (text or "").strip()
    if not t:
        raise RuntimeError("OpenAI returned empty response")

    # Strip occasional fenced JSON
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```\s*$", t, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()

    try:
        data = json.loads(t)
    except json.JSONDecodeError:
        # one-shot repair
        fixed = _repair_json_once(text)
        try:
            data = json.loads(fixed)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"OpenAI response was not valid JSON (even after repair):\n{text}") from e

    if not isinstance(data, dict):
        raise RuntimeError("Invalid response: top-level must be an object")
    # Normalize model type drift deterministically.
    # The contract allows only: "keyword" or "tool".
    def _normalize_keyword_scout_types(obj: dict) -> None:
        items = obj.get("keywords_tools_ranked")
        if not isinstance(items, list):
            return
        for it in items:
            if not isinstance(it, dict):
                continue
            t = (it.get("type") or "").strip().lower()
            if t == "tool":
                it["type"] = "tool"
            else:
                # anything else becomes keyword (protocol, language, etc.)
                it["type"] = "keyword"

    _normalize_keyword_scout_types(data)

    return data
