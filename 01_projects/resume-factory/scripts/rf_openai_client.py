from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from rf_proposal_schema import json_schema_for_structured_outputs

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
    """
    Calls OpenAI and returns proposals list (already schema-constrained by Structured Outputs).
    """
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)

    model = model or _env("RF_OPENAI_MODEL", "gpt-4o-mini")

    sys = (
        "You generate localized edit proposals for a resume.\n"
        "Hard rules:\n"
        "- Output MUST match the provided JSON schema exactly.\n"
        "- AI proposes only. Do NOT apply edits.\n"
        "- Proposals must be localized and safe.\n"
        "- Use REPLACE_PHRASE unless a full-line replacement is truly required.\n"
        "- The 'before' string MUST appear verbatim in the provided resume text blocks.\n"
        "- Do not invent content that is not grounded in the JD.\n"
        "- Do not add new sections; only adjust existing content.\n"
        "- Prefer <= {max_proposals} proposals.\n"
    ).format(max_proposals=max_proposals)

    # Keep the user prompt extremely explicit about "before must exist"
    usr = (
        "JOB DESCRIPTION (raw):\n"
        "-----\n"
        f"{jd_raw.strip()}\n"
        "-----\n\n"
        "TEMPLATE SIGNALS (json):\n"
        "-----\n"
        f"{signals}\n"
        "-----\n\n"
        "RESUME TEXT BLOCKS (authoritative; use exact substrings from here):\n"
        "-----\n"
        f"{resume_blocks.strip()}\n"
        "-----\n\n"
        "Task:\n"
        "- Identify gaps between JD and resume.\n"
        "- Propose localized edits using ONLY these ops:\n"
        "  - REPLACE_PHRASE: replace a short phrase that already exists\n"
        "  - REPLACE_LINE: replace an entire line if phrase replacement cannot work\n"
        "- Each proposal:\n"
        "  - section: SUMMARY|SKILLS|EXPERIENCE\n"
        "  - before: [single exact string from RESUME TEXT BLOCKS]\n"
        "  - after: [single replacement string]\n"
        "  - rationale: short justification referencing JD needs\n"
        "- Do NOT propose edits where 'before' does not exist verbatim in RESUME TEXT BLOCKS.\n"
        "- Avoid big rewrites; keep changes minimal.\n"
    )

    schema = json_schema_for_structured_outputs()

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": schema,
        },
    )

    # In the Python SDK, Structured Outputs returns a parsed object in output_text sometimes,
    # but the most reliable approach is to read resp.output[0].content[0].parsed when present.
    # We'll handle both defensively.
    parsed = None

    try:
        # Newer SDKs: parsed object is attached to the first content item
        for out in resp.output:
            for c in out.content:
                if hasattr(c, "parsed") and c.parsed is not None:
                    parsed = c.parsed
                    break
            if parsed is not None:
                break
    except Exception:
        parsed = None

    if parsed is None:
        # Fallback: attempt to treat output_text as JSON string (rare in strict schema mode)
        txt = getattr(resp, "output_text", None)
        if not txt:
            raise RuntimeError("OpenAI response missing parsed content")
        import json
        parsed = json.loads(txt)

    proposals = parsed.get("proposals", [])
    return proposals
