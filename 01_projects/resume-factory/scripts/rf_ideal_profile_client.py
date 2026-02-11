from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Optional

from openai import OpenAI
from openai import RateLimitError, AuthenticationError


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    return v if (v is not None and v != "") else default


def _require(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"missing required env var: {name}")
    return v


def ideal_profile_openai(
    *,
    jd_raw: str,
    keyword_scout: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
    timeout_s: int = 90,
    extra_instructions: str = "",
) -> Dict[str, Any]:
    _require("OPENAI_API_KEY")
    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_IDEAL_PROFILE_MODEL", "gpt-4o-mini")

    system_prompt = """You are Resume Factory - Ideal Profile Generator.

GOAL:
- Read the JD and produce an ideal candidate profile to guide resume rewriting.
- Infer what the hiring manager truly wants; do not hallucinate tools.
- If keyword_scout is provided, use it as a signal, not a constraint.

OUTPUT RULES:
- Return STRICT JSON ONLY (no markdown, no commentary).
- Keep lists concise, high-signal, and non-redundant.

JSON CONTRACT:
{
  "ideal_profile": {
    "must_haves": ["..."],
    "nice_to_haves": ["..."],
    "domain_context": ["..."],
    "core_responsibilities": ["..."],
    "signals_of_seniority": ["..."],
    "risks_red_flags": ["..."]
  },
  "notes": ""
}
"""

    ks = keyword_scout or {}
    ks_json = json.dumps(ks, indent=2) if ks else "(none)"

    user_prompt = f"""JOB DESCRIPTION (source of truth):
{jd_raw}

KEYWORD SCOUT (optional hint):
{ks_json}

EXTRA INSTRUCTIONS:
{extra_instructions}

TASK:
Return the JSON contract only."""

    def _repair_json_once(bad_text: str) -> str:
        repair_system = """You are a JSON repair bot.
RULES:
- Output STRICT JSON ONLY.
- Do NOT add or remove items.
- Do NOT change meaning.
- Fix syntax only.
"""
        repair_user = f"""Fix this into valid JSON (syntax repair only):

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
        out = out.strip()
        m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", out, flags=re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else out

    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
        )
    except AuthenticationError as e:
        raise RuntimeError("OpenAI auth failed.") from e
    except RateLimitError as e:
        raise RuntimeError("OpenAI rate limit or quota error.") from e

    text = ""
    for o in resp.output:
        for c in o.content:
            if c.type == "output_text":
                text += c.text
    t = text.strip()
    if not t:
        raise RuntimeError("Empty OpenAI response")

    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", t, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()

    try:
        data = json.loads(t)
    except json.JSONDecodeError:
        fixed = _repair_json_once(text)
        data = json.loads(fixed)

    if not isinstance(data, dict):
        raise RuntimeError("Top-level JSON must be an object")

    return data
