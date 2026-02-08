from __future__ import annotations

import json
import re
import os
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


def _load_rf_prompt() -> str:
    """
    Canonical prompt template loader.
    Source of truth: 01_projects/resume-factory/AGENT_PROMPT.md
    (rf-prompt is a CLI helper script, not the prompt text.)
    """
    candidates = [
        os.path.expanduser("~/secondbrain/01_projects/resume-factory/AGENT_PROMPT.md"),
        os.path.expanduser("~/secondbrain/01_projects/resume-factory/AGENTS.md"),
    ]
    for path in candidates:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
    raise RuntimeError(
        "Canonical prompt not found. Expected one of:\n"
        + "\n".join(f"- {c}" for c in candidates)
    )


def _detect_primary_stack(jd_text: str) -> Dict[str, str]:
    """
    Deterministic, lightweight detection of the JD's primary automation stack.
    This is a hint to the model to avoid mixed-stack incoherence.
    """
    t = (jd_text or "").lower()

    # Primary tool/framework (pick strongest signal)
    tool = ""
    if re.search(r"\bcypress\b", t):
        tool = "cypress"
    elif re.search(r"\bplaywright\b", t):
        tool = "playwright"
    elif re.search(r"\bselenium\b", t):
        tool = "selenium"
    elif re.search(r"\bwebdriverio\b", t):
        tool = "webdriverio"
    elif re.search(r"\bpuppeteer\b", t):
        tool = "puppeteer"

    # Primary language (pick strongest signal)
    lang = ""
    if re.search(r"\btypescript\b", t):
        lang = "typescript"
    elif re.search(r"\bjavascript\b", t):
        lang = "javascript"
    elif re.search(r"\bjava\b", t):
        lang = "java"
    elif re.search(r"\bc#\b|\bc sharp\b", t):
        lang = "c#"
    elif re.search(r"\bpython\b", t):
        lang = "python"

    return {"tool": tool, "language": lang}




def generate_rewrite_packet_openai(
    *,
    jd_raw: str,
    resume_blocks_numbered: str,
    signals: Dict[str, Any],
    selected_template: str,
    model: Optional[str] = None,
    max_proposals: int = 16,
    timeout_s: int = 90,
) -> Dict[str, Any]:
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)
    model = model or _env("RF_OPENAI_MODEL", "gpt-4o-mini")
    rf_prompt = _load_rf_prompt()

    primary_stack = _detect_primary_stack(jd_raw)

    # Keep this ASCII-only and avoid raw JSON braces inside f-strings.
    contract_text = (
        "OUTPUT CONTRACT (v0) — MUST MATCH EXACTLY:\n"
        "{\n"
        '  "selected_template": "<template folder name>",\n'
        '  "rewrite_packet": {\n'
        '    "professional_summary": ["<line1>", "<line2>", "..."] OR "<multi-line block>",\n'
        '    "technical_skills": ["<line1>", "<line2>", "..."],\n'
        '    "experience": [\n'
        '      { "target": "E###", "action": "REPLACE_LINE", "new_line": "• <new bullet line text>" }\n'
        "    ],\n"
        '    "notes": "<optional blunt reasoning / scan test / risks>"\n'
        "  }\n"
        "}\n"
    )

    system_prompt = f"""You are the Resume Factory - LLM Rewrite Engine.

GOVERNANCE:
- Follow the canonical rf-prompt (embedded below) as the primary behavioral contract.
- Output MUST be strict JSON ONLY. No markdown. No trailing text.
- Your JSON must parse via json.loads() with no cleanup.

CANONICAL RF-PROMPT (verbatim):
{rf_prompt}

{contract_text}

HARD RULES:
- selected_template MUST equal the provided template folder name EXACTLY.
- Return ONLY the JSON object. Do not wrap in markdown fences.
- No freeform commentary outside rewrite_packet.notes.

LIMITS:
- Prefer high-signal edits; do not rewrite everything.
"""

    user_prompt = f"""PRIMARY STACK TARGET (deterministic; obey for coherence):
- tool: {primary_stack.get("tool","")}
- language: {primary_stack.get("language","")}

TEMPLATE FOLDER (MUST ECHO IN selected_template):
{selected_template}

JOB DESCRIPTION:
{jd_raw}

TEMPLATE SIGNALS (json):
{json.dumps(signals, indent=2)}

RESUME TEXT (numbered; choose targets from here):
{resume_blocks_numbered}

TASK:
Generate a rewrite packet only (v0 contract). Do not generate proposals; the CLI will compile deterministic proposals from your rewrite_packet.
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

    # Some models occasionally wrap JSON in markdown fences. Strip them deterministically.
    t = text.strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```\s*$", t, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()

    try:
        data = json.loads(t)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"OpenAI response was not valid JSON:\n{text}") from e

    if not isinstance(data, dict):
        raise RuntimeError("Invalid response shape: top-level must be an object")

    for k in ("selected_template", "rewrite_packet"):
        if k not in data:
            raise RuntimeError(f"Invalid response contract: missing key {k!r}")

    return data
