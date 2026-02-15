import json
import os
import re
from typing import Any, Dict, Optional

from openai import OpenAI
from openai import RateLimitError, AuthenticationError


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    # remove leading/trailing triple-backtick fences if present
    # supports ```json ... ``` or ``` ... ```
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
        t = re.sub(r"\s*```$", "", t)
    return t.strip()

def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    return v if (v is not None and v != "") else default

def _require(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"missing required env var: {name}")
    return v

def ai_parse_job_openai(
    *,
    page_title: Optional[str],
    page_text: str,
    source_url: str,
    model: Optional[str] = None,
    timeout_s: int = 60,
) -> Dict[str, Any]:
    """
    Returns JSON dict with keys:
      company (string, required)
      role_title (string, required)
      description (string, required)
      location (string|null)
      source (string, required)
    """
    _require("OPENAI_API_KEY")

    client = OpenAI(timeout=timeout_s)
    model = model or _env("JOB_INTAKE_OPENAI_MODEL", _env("RF_OPENAI_MODEL", "gpt-4o-mini"))

    # keep prompt bounded (avoid huge pages)
    text = (page_text or "").strip()
    if len(text) > 20000:
        text = text[:20000]

    system_prompt = """
You extract structured job posting fields from messy web page text.

ABSOLUTE RULES:
- Output ONLY valid JSON.
- No markdown.
- No commentary.
- No trailing text.
- JSON must parse via json.loads().

FIELD RULES:
- company: required string (best guess; do not include board name like "Dice" unless truly the employer)
- role_title: required string with correct casing
- description: required string; the cleaned job description (remove nav/footer noise as best you can)
- location: optional string or null
- source: required string (must equal SOURCE_URL exactly)
"""

    user_prompt = f"""
SOURCE_URL (must copy EXACTLY into output.source):
{source_url}

PAGE_TITLE (may be noisy):
{page_title or ""}

RAW_PAGE_TEXT:
{text}

TASK:
Return JSON with: company, role_title, description, location, source.
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
        raise RuntimeError("OpenAI auth failed (check OPENAI_API_KEY).") from e
    except RateLimitError as e:
        msg = str(e)
        if "insufficient_quota" in msg or "check your plan and billing details" in msg:
            raise RuntimeError("OpenAI quota/billing blocked this request (insufficient_quota).") from e
        raise

    text_out = ""
    for out in resp.output:
        for c in out.content:
            if c.type == "output_text":
                text_out += c.text

    text_out = (text_out or "").strip()
    if not text_out:
        raise RuntimeError("OpenAI returned empty response")

    text_out = _strip_code_fences(text_out)

    try:
        data = json.loads(text_out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"OpenAI response was not valid JSON:\n{text_out}") from e

    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid response type: {type(data)}")

    # validate required fields
    for k in ["company", "role_title", "description", "source"]:
        if k not in data or not isinstance(data[k], str) or not data[k].strip():
            raise RuntimeError(f"Missing/invalid required field: {k}")

    if data["source"].strip() != source_url:
        raise RuntimeError("Invalid source: must exactly match SOURCE_URL")

    # normalize optional
    loc = data.get("location", None)
    if loc is not None and not (isinstance(loc, str) and loc.strip()):
        data["location"] = None

    return data
