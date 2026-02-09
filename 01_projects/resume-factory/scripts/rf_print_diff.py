from __future__ import annotations

from typing import Any, Dict, List

def print_diff(proposals: List[Dict[str, Any]]) -> None:
    """
    Terminal-friendly BEFORE/AFTER blocks.
    Numbering is implicit (1..N) to match resume-approve-edits selection UX.
    """
    if not proposals:
        print("Proposed localized edits (READ-ONLY): none.\n")
        return

    print("Proposed localized edits (READ-ONLY):\n")
    for i, p in enumerate(proposals, start=1):
        sec = p.get("section", "?")
        op = p.get("op", "?")
        rationale = (p.get("rationale") or "").strip()

        before = p.get("before") or []
        after = p.get("after") or []

        rr = p.get("subsection_occurrence")
        rr_tag = f" (RR#{rr})" if rr else ""
        print(f"{i}. [{sec}] {op}{rr_tag}")
        if rationale:
            print(f"   why: {rationale}")

        print("   BEFORE:")
        for line in before:
            print(f"   - {line}")

        print("   AFTER:")
        for line in after:
            print(f"   + {line}")

        print()
