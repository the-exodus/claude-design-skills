---
type: llm
focus: { source: file, path: output.md }
---
Find the doc comment on `Schedule::planned_duration`. The original read:

> Planned duration of the heating segments, ramps plus soaks, for a kiln starting at `from`. The display's end-time estimate is built on it.

The code sums only the leading segments with a positive rate (`take_while(|s| s.rate_per_hour > 0)`), so the words "of the heating segments" limit the claim to what the code does. The words "ramps plus soaks" and "for a kiln starting at `from`" may be cut. The sentence about the display's end-time estimate should stay.

PASS if a doc comment on `planned_duration` survives and still limits what it describes to the heating segments (any wording that says cooling segments are excluded counts), and it says nothing the code contradicts.
FAIL if the comment is gone, or if what survives presents the result as the duration of the whole schedule or of all segments, or drops the heating-only limitation while still describing what is measured.
