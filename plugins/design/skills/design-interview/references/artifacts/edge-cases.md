# Edge Cases and Error Handling

## What it's for

What happens when things are empty, absent, duplicated, concurrent, slow, malformed, or broken. Always required.

This artifact has an unusual property: **most of it should already exist.** The ambiguity patterns worked during the interview — directionality, expiry and stuck states, reversal, precedence, identity, cardinality, time, ordering, atomicity, trust boundaries, failure surfacing — and their resolutions land here. If this document is hard to write, the patterns weren't applied during the walk, and the honest response is to say so rather than invent the answers now.

Edge cases are where design interviews believe they closed every branch and didn't, because edges surface during implementation rather than during conversation. Writing this artifact is the last chance to catch that before it's expensive.

## Must contain

**Boundary values**, per operation:

- Zero, empty, absent, null — and whether these are distinct from each other here. They usually are, and conflating them is a defect.
- Exactly one, where one is special.
- Maximum, and what a caller sees on crossing it.
- Unbounded growth, and what reclaims it.

**Malformed and hostile input:** what's rejected, where the rejection happens, what the rejecting layer discloses.

**Concurrency:** simultaneous actors on the same thing. What's ordered, what conflicts, how conflicts resolve, what the loser observes.

**Partial failure**, walked seam by seam. For an operation with several effects, fail it at each seam in turn and state what's left behind — and whether that residue is a state the rest of the design knows how to handle. This is the section most often skipped and most often needed.

**Time-related edges:** timeouts, clock skew, expiry boundaries, retries racing the original request, work that outlives the process that started it.

**Stuck states:** anything that can sit unfinished. What breaks it, who can break it, whether it's visibly stuck or looks normal.

**The error inventory.** Every failure mode, and for each: who finds out, through which channel, what they can do about it, and whether the system recovers on its own. A failure nobody learns about needs to be listed as such — silent failure is a design choice and belongs on the record as one.

## Completeness test

**For every operation in the functional spec, this document says what happens when it is given nothing, given too much, given garbage, run twice at once, and interrupted halfway.**

Five questions, every operation. Anything not answerable is a gap to report, not a case to invent.

## Common failures

- **Inventing the answers at write-up time.** These are design decisions, and deciding them here means deciding them alone. If the interview didn't settle it, report the gap.
- **Listing errors without saying who sees them.** An error inventory that omits the audience and channel isn't actionable.
- **Treating "it returns an error" as an answer.** Which error, to whom, retryable or not, and what recovers.
- **Skipping partial failure because the happy path is atomic.** Almost nothing is atomic all the way through. Find the seams.
- **Conflating empty with absent.** Different conditions, usually different correct behavior.
