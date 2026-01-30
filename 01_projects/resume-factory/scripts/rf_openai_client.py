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
    resume_blocks_numbered: str,
    signals: Dict[str, Any],
    jd_terms: List[str],
    model: Optional[str] = None,
    max_proposals: int = 12,
    timeout_s: int = 60,
) -> List[Dict[str, Any]]:
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_OPENAI_MODEL", "gpt-4o-mini")

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

YOU MUST ANCHOR EVERY PROPOSAL TO AN EXISTING NUMBERED RESUME LINE:
- Choose "before_ref" from the numbered RESUME text (e.g., S003, K012, E044).
- The "before" value MUST be the exact text of that referenced line (copy it exactly, without the "S003 |" prefix).
- Copy/paste the before line exactly. Do not paraphrase it. If you can’t copy it exactly, skip that line.
- In the drop notes, print before_ref too so you can quickly spot where it’s failing.

YOU MUST GROUND EVERY PROPOSAL IN THE JD TERMS LIST:
- Each proposal must include "jd_term" set to EXACTLY one item from JD_TERMS.
- The rationale must begin exactly:
  "JD mentions <jd_term>; align resume to JD requirement."

COLLISION RULE (IMPORTANT):
- Do NOT output more than one proposal with the same before_ref.
- Do NOT output more than one proposal for the same before_ref.
- If you need to address multiple JD_TERMS on the same resume line, combine them into a single updated after[0] for that before_ref.
- If multiple JD_TERMS apply to the same resume line, combine them into ONE updated after[0] for that before_ref.

QUALITY RULES (MANDATORY):
- Do NOT append vague meta phrases like "reinforcing", "addressing", "essential for", "best practices", "within the lifecycle".
- Every edit must add concrete, test-relevant content: a method, artifact, tool, or measurable action.
- If you cannot add concrete content without changing meaning, SKIP that line and choose a different before_ref.

TERM-SPECIFIC RULES:
- For risks/dependencies: mention risk-based testing, dependency mapping, release blockers, or documenting risks in test plans (not just the words "risks/dependencies").
- For performance/load/stress: mention JMeter/k6/Gatling OR "load/stress" explicitly in a technically natural way (not "workflows").
- For design/implementation: reference framework design, architecture, POM, utilities, or implementation of automation components (not "best practices").

UI/UX TARGETING RULE:
- If jd_term is "ui/ux", you MUST anchor to a line that already mentions UI, UX, accessibility, WCAG, Axe, WAVE, ARIA, frontend, or user experience.
- If no such line exists, do NOT propose a change for ui/ux.

LINE MERGE RULE (CRITICAL):
- You may propose AT MOST ONE change per resume line (before_ref).
- If multiple JD terms apply to the same line, you MUST combine them into a single AFTER rewrite.
- Do NOT create multiple proposals that target the same before_ref.
- When combining multiple JD terms into a single edit, prefer REPLACE_LINE over REPLACE_PHRASE.
EXAMPLE:
If a line already covers regression testing and the JD adds "performance/load" and "risks/dependencies",
combine them into ONE sentence that naturally incorporates both.

JSON SHAPE:
{{
  "proposals": [
    {{
      "section": "SUMMARY|SKILLS|EXPERIENCE",
      "op": "REPLACE_PHRASE|REPLACE_LINE",
      "before_ref": "S001|K001|E001 ...",
      "before": ["<exact line text from before_ref>"],
      "after": ["<replacement string>"],
      "jd_term": "<one term from JD_TERMS>",
      "rationale": "JD mentions <jd_term>; align resume to JD requirement. <short detail>"
    }}
  ]
}}

CONSTRAINTS:
- Propose at most {max_proposals} items.
- Prefer REPLACE_PHRASE unless the entire line needs replacement.
- Keep meaning close to the original line (minimal semantic drift).
- Avoid generic style edits (clarity/impact/assertiveness). Every change must be JD alignment.
- Do not introduce filler like proactively, actively, hands-on, involved. Only add concrete technical content.
- If a JD term is not a tool/technology, do not force it into EXPERIENCE. Prefer SKILLS or skip.
"""

    user_prompt = f"""
JD_TERMS (must choose from; do not invent new terms):
{json.dumps(jd_terms, indent=2)}

JOB DESCRIPTION:
{jd_raw}

TEMPLATE SIGNALS (json):
{json.dumps(signals, indent=2)}

RESUME TEXT (numbered; pick before_ref from here and copy its exact line text into before[0]):
{resume_blocks_numbered}

TASK:
Propose JD-aligned edits. Anchor each proposal to an existing numbered resume line.
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
