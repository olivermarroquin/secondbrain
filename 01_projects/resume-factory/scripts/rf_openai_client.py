from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

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

def propose_edits_openai(
    *,
    jd_raw: str,
    resume_blocks: str,
    signals: Dict[str, Any],
    jd_terms: List[str],
    model: Optional[str] = None,
    max_proposals: int = 12,
    timeout_s: int = 60,
) -> List[Dict[str, Any]]:
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_OPENAI_MODEL", "gpt-4o-mini")

    # Keep terms short + stable
    jd_terms = [t.strip() for t in (jd_terms or []) if isinstance(t, str) and t.strip()]
    jd_terms = jd_terms[:30]

    system_prompt = f"""
You generate localized edit proposals for a resume.

ABSOLUTE RULES:
- Output ONLY valid JSON.
- No markdown.
- No commentary.
- No trailing text.
- JSON must parse via json.loads().

YOU MUST GROUND EVERY PROPOSAL IN THE JD TERMS LIST.
- Each proposal must include "jd_term" set to EXACTLY one item from the provided JD_TERMS list.
- The "rationale" must begin with: "JD mentions <jd_term>; ..."
  where <jd_term> matches the proposal's jd_term EXACTLY (case-insensitive match is ok, but keep spelling identical).

JSON SHAPE:
{{
  "proposals": [
    {{
      "section": "SUMMARY|SKILLS|EXPERIENCE",
      "op": "REPLACE_PHRASE|REPLACE_LINE",
      "before": ["exact string that already exists in RESUME TEXT"],
      "after": ["replacement string"],
      "jd_term": "<one term from JD_TERMS>",
      "rationale": "JD mentions <jd_term>; <short, concrete reason tied to JD>"
    }}
  ]
}}

CONSTRAINTS:
- Propose at most {max_proposals} items.
- 'before' MUST appear verbatim in the resume text (exact substring).
- Prefer REPLACE_PHRASE. Use REPLACE_LINE only if needed.
- Do NOT invent tools/terms not present in the JD_TERMS list.
- Do NOT apply edits.
"""

    user_prompt = f"""
JD_TERMS (must choose from; do not invent new terms):
{json.dumps(jd_terms, indent=2)}

JOB DESCRIPTION:
{jd_raw}

TEMPLATE SIGNALS (json):
{json.dumps(signals, indent=2)}

RESUME TEXT (authoritative; 'before' must be exact substring from here):
{resume_blocks}

TASK:
Identify JD gaps and propose safe, localized edits grounded in JD_TERMS.
"""

    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
        )
    except AuthenticationError as e:
        raise RuntimeError(
            "OpenAI auth failed (invalid API key). Recreate the key and re-export OPENAI_API_KEY."
        ) from e
    except RateLimitError as e:
        msg = str(e)
        if "insufficient_quota" in msg or "check your plan and billing details" in msg:
            raise RuntimeError(
                "OpenAI quota/billing blocked this request (insufficient_quota). "
                "Fix: enable billing or add prepaid credits in the OpenAI dashboard, then rerun."
            ) from e
        raise

    text = ""
    for out in resp.output:
        for c in out.content:
            if c.type == "output_text":
                text += c.text

    text = text.strip()
    if not text:
        raise RuntimeError("OpenAI returned empty response")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"OpenAI response was not valid JSON:\n{text}") from e

    if not isinstance(data, dict) or "proposals" not in data:
        raise RuntimeError(f"Invalid response shape: {data}")

    return data["proposals"]
