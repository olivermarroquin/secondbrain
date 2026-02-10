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

def keyword_scout_openai(
    *,
    jd_raw: str,
    baseline_text: str = "",
    baseline_covered_terms: Optional[list] = None,
    model: Optional[str] = None,
    timeout_s: int = 90,
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
Return the JSON contract. Pick the best 10–20 keywords/tools and 3–7 implied responsibilities/flows."""
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
    except json.JSONDecodeError as e:
        raise RuntimeError(f"OpenAI response was not valid JSON:\n{text}") from e

    if not isinstance(data, dict):
        raise RuntimeError("Invalid response: top-level must be an object")

    return data
