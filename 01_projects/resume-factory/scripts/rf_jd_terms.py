from __future__ import annotations

import re
from collections import Counter
from typing import List, Set, Tuple

def _norm(s: str) -> str:
    s = (s or "")
    s = s.replace("\u2019", "'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _low(s: str) -> str:
    return _norm(s).lower()

def _canonical(term: str) -> str:
    t = _low(term)
    replacements = {
        "cicd": "ci/cd",
        "ci cd": "ci/cd",
        "rest-assured": "rest assured",
        "test rail": "testrail",
        "as a full-stack": "full-stack",
        "a full-stack": "full-stack",
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    return t.strip()

def _is_toolish(token: str) -> bool:
    if any(ch in token for ch in ["/", ".", "-", "_"]):
        return True
    if any(ch.isdigit() for ch in token):
        return True
    return False

TRIVIAL_ABBREVIATIONS = {"e.g", "eg", "i.e", "ie"}
EMPLOYMENT_MARKETING = {"full-time", "contract/temporary", "ai-matched", "ai-powered"}
LEGAL_HR = {"eeo", "equal opportunity", "disability", "veterans", "m/f/"}
GENERIC_VERB_FRAGMENTS = {"build/maintain", "establish/enforce", "to succeed"}

# Explicit junk tokens observed in real JDs (keep this list tight and auditable)
EXPLICIT_JUNK_TERMS = {
    "education/certification",
    "stack-ranked",
    "required -",
    "required.-",
    "required. -",
    "ad",
    "ai",
}

def _is_junk(term: str) -> bool:
    t = term.strip()
    if not t:
        return True

    # normalize for comparisons
    tl = t.lower()

    # exact junk terms
    if tl in EXPLICIT_JUNK_TERMS:
        return True

    # trivial abbreviations
    if tl in TRIVIAL_ABBREVIATIONS:
        return True

    # employment / marketing artifacts
    if tl in EMPLOYMENT_MARKETING:
        return True

    # HR / legal boilerplate
    if any(x in tl for x in LEGAL_HR):
        return True

    # generic verb fragments
    if any(x in tl for x in GENERIC_VERB_FRAGMENTS):
        return True

    # years (e.g. 2024)
    if re.fullmatch(r"20\d{2}", tl):
        return True

    # money/benefits tokens (401k, etc.)
    if re.fullmatch(r"\d{3,4}k", tl):
        return True

    # decimals / rates (53.85, 63.85)
    if re.fullmatch(r"\d+\.\d+", tl):
        return True

    # times (8am, 5pm)
    if re.fullmatch(r"\d{1,2}(am|pm)", tl):
        return True

    # ranges like 5-7 (years), 1-2, etc.
    if re.fullmatch(r"\d{1,2}-\d{1,2}", tl):
        return True

    # pure numbers (30, 12)
    if re.fullmatch(r"\d+", tl):
        return True

    # alphanumeric IDs (cxsapwma1)
    if re.fullmatch(r"[a-z]{3,}\d+[a-z0-9]*", tl):
        return True

    # formatting artifacts: trailing punctuation/dashes
    if re.search(r"[.\-]{2,}", tl):
        return True
    if re.fullmatch(r".*-\s*$", tl):
        return True

    # hyphenated adjective junk (high-quality, must-have, short-term)
    if tl in {"high-quality", "must-have", "short-term"}:
        return True

    # URLs / domains
    if any(x in tl for x in ("http", ".com", ".net", ".org")):
        return True

    # numeric identifiers
    if re.fullmatch(r"[0-9\-]{6,}", tl):
        return True

    # overly long / sentence-like fragments
    if len(tl) > 25:
        return True
    if len(tl.split()) > 3:
        return True

    return False

def extract_jd_terms(jd_raw: str, max_terms: int = 30) -> List[str]:
    raw = jd_raw or ""
    txt = _norm(raw)
    low = txt.lower()

    candidates: List[str] = []

    acronyms = re.findall(r"\b[A-Z]{2,}\b", raw)
    for a in acronyms:
        candidates.append(_canonical(a))

    if "ci/cd" not in candidates and ("CI" in acronyms and "CD" in acronyms):
        candidates.append("ci/cd")

    toolish_tokens = re.findall(r"\b[\w\./_-]+[0-9\./_-]*[\w]+[\w\./_-]*\b", txt)
    for tok in toolish_tokens:
        tt = _canonical(tok)
        if len(tt) >= 2 and _is_toolish(tt):
            candidates.append(tt)

    words = re.findall(r"[a-zA-Z0-9\./_-]+", txt)
    words_l = [_canonical(w) for w in words if w.strip()]

    bigrams = [" ".join(words_l[i:i+2]) for i in range(len(words_l) - 1)]
    trigrams = [" ".join(words_l[i:i+3]) for i in range(len(words_l) - 2)]

    bg_counts = Counter(bigrams)
    tg_counts = Counter(trigrams)

    for phrase, count in bg_counts.items():
        if count >= 2 and any(_is_toolish(w) for w in phrase.split()):
            candidates.append(_canonical(phrase))

    for phrase, count in tg_counts.items():
        if count >= 2 and any(_is_toolish(w) for w in phrase.split()):
            candidates.append(_canonical(phrase))

    uniq: List[str] = []
    seen: Set[str] = set()

    for tt in candidates:
        if not tt or tt in seen:
            continue
        if _is_junk(tt):
            continue
        seen.add(tt)
        uniq.append(tt)

    def score(term: str) -> Tuple[int, int]:
        freq = low.count(term)
        bonus = 2 if any(_is_toolish(w) for w in term.split()) else 0
        return (freq + bonus, len(term))

    uniq.sort(key=score, reverse=True)
    return uniq[:max_terms]

def rationale_mentions_term(rationale: str, terms: List[str]) -> bool:
    r = _low(rationale)
    return any(t in r for t in terms if t)
