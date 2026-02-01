Reviewed File:
- java/_001_TwoSum.java

What Works:
- Uses a HashMap for O(n) lookup and returns indices as soon as a complement is found.
- Correctly avoids reusing the same element by inserting into the map after the check.
- Matches the problem’s “exactly one solution” assumption with a straightforward return.

Issues:
- The method returns an empty array when no solution is found, which is inconsistent with the “exactly one solution” assumption and gives no signal to callers if the input is invalid.

Improvements:
- Consider throwing an IllegalArgumentException (or similar) if no solution is found to make invalid inputs explicit.
- Optionally pre-size the HashMap with `nums.length` for slightly better performance on large arrays.

Concepts to Review:
- HashMap time/space tradeoffs and when early return is safe.
- API design for invalid inputs (empty array vs exception).

Next Action:
- Decide whether to enforce the “exactly one solution” contract by throwing an exception instead of returning an empty array.

Files Changed:
- reviews/001_two_sum_review.md
