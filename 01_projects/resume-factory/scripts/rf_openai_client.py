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
    model: Optional[str] = None,
    max_proposals: int = 12,
    timeout_s: int = 60,
) -> List[Dict[str, Any]]:
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_OPENAI_MODEL", "gpt-4o-mini")

    system_prompt = f"""
You generate localized edit proposals for a resume.

ABSOLUTE RULES:
- Output ONLY valid JSON.
- No markdown.
- No commentary.
- No trailing text.
- The JSON must parse with json.loads().

JSON SHAPE:
{{
  "proposals": [
    {{
      "section": "SUMMARY|SKILLS|EXPERIENCE",
      "op": "REPLACE_PHRASE|REPLACE_LINE",
      "before": ["exact string that already exists"],
      "after": ["replacement string"],
      "rationale": "short justification"
    }}
  ]
}}

CONSTRAINTS:
- Propose at most {max_proposals} items.
- 'before' MUST appear verbatim in the resume text.
- Prefer REPLACE_PHRASE.
- Do NOT invent new sections.
- Do NOT apply edits.
"""

    user_prompt = f"""
JOB DESCRIPTION:
{jd_raw}

TEMPLATE SIGNALS (json):
{json.dumps(signals, indent=2)}

RESUME TEXT (authoritative):
{resume_blocks}

TASK:
Identify gaps and propose safe, localized edits.
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
        # OpenAI uses RateLimitError for both rate limits and insufficient_quota.
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
