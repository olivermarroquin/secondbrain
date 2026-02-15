import os
import re
from typing import Optional, Dict
from openai import OpenAI, AuthenticationError, RateLimitError

def _require(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"missing required env var: {name}")
    return v

def extract_jd_openai(page_text: str, model: Optional[str] = None, timeout_s: int = 60) -> str:
    """
    Uses an LLM to extract only the job description from noisy scraped text.
    Returns plain text description.
    """
    _require("OPENAI_API_KEY")
    client = OpenAI(timeout=timeout_s)
    model = model or os.environ.get("RF_OPENAI_MODEL", "gpt-4o-mini")

    # truncate if very long
    text = (page_text or "").strip()
    if len(text) > 20000:
        text = text[:20000]

    system_prompt = """
You are a parser that extracts only the main job description from a scraped web page.
Ignore headers, footers, navigation, ads, and any unrelated content.
Return ONLY the job description text as plain text.
Do NOT include markdown, JSON, or code fences.
"""
    user_prompt = f"""
RAW_PAGE_TEXT:
{text}

TASK:
Return only the job description.
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
        raise RuntimeError("JD extraction LLM returned empty text")

    # remove any code fences
    if text_out.startswith("```"):
        text_out = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", text_out)
        text_out = re.sub(r"\s*```$", "", text_out)

    return text_out.strip()
