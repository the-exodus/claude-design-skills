# ADR format reference

A complete worked set lives in `examples/`: an Accepted ADR with an addendum, a
superseded ADR and the ADR that supersedes it, a rejected proposal, and the index
that lists all four.

## Template

```markdown
# ADR-NNNN — Title stating the decision

**Status:** Proposed (YYYY-MM-DD)

## Context

The situation that forces a decision: the constraints that apply, what is
already true, what was measured. Enough for a reader years later to judge
whether those constraints still hold.

## Decision

What was decided, in the active voice. Alternatives that were rejected go here,
with the reason they were rejected.

## Consequences

What follows from the decision — what becomes possible, what becomes harder,
what work it creates, what it forecloses. Both directions, not only the
favourable one.
```

Sections appended after Consequences, in date order:

```markdown
## Addendum YYYY-MM-DD

What is new, and why the decision stands with it.
```

```markdown
## Rejection

Why the proposal was turned down, and what is done instead.
```

## Header grammar

The status line is one line, fields separated by ` · `. `NNNN-slug.md` stands
for the target ADR's filename.

| Case | Status line |
|------|-------------|
| Proposed | `**Status:** Proposed (2026-06-18)` |
| Accepted | `**Status:** Accepted (2026-06-18)` |
| Accepted, supersedes | `**Status:** Accepted (2026-06-18) · **Supersedes:** [ADR-0002](NNNN-slug.md)` |
| Rejected | `**Status:** Rejected (2026-06-18)` |
| Superseded | `**Status:** Superseded by [ADR-0004](NNNN-slug.md) (2026-06-18)` |
| Deprecated | `**Status:** Deprecated (2026-06-18) — no longer applies; not replaced` |
| Retrospective | `**Status:** Accepted (retrospective, 2026-06-18)` |
| Existing ADR, one of its decisions superseded | `**Status:** Accepted (2025-02-03); partly superseded by [ADR-0012](NNNN-slug.md) (publisher identity, 2026-06-18)` |
| New ADR, supersedes one decision in an existing ADR | `**Status:** Accepted (2026-06-18) · **Supersedes:** the publisher identity decision in [ADR-0007](NNNN-slug.md)` |

The date is the date the status was reached, not the date of the edit. A
retrospective ADR reaches Accepted on the day it is written.

The last two rows are the two sides of one supersede: ADR-0012 takes over one
decision from ADR-0007. They apply only when the superseded ADR is in another
format and records several decisions. An existing ADR whose status lives in a
bare `Status:` line or a `## Status` section takes the same `partly superseded
by` text there.

Projects that track decisions against an issue tracker, epic, or ticket can add
a field of their own to this line using the same ` · ` separator. Nothing here
assumes one exists.

## Index table

`README.md`, in the same directory as the ADRs — the full file is in
`examples/README.md`.

```markdown
## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-slug.md) | Title stating the decision | Accepted |
| [0002](0002-slug.md) | Title stating the decision | Superseded by ADR-0004 |
| [0003](0003-slug.md) | Title stating the decision | Rejected |
| [0004](0004-slug.md) | Title stating the decision | Accepted |
```

Superseded and rejected rows keep their number and title and carry the outcome
in the Status column. A partly superseded existing ADR reads `<its status>;
partly superseded by ADR-NNNN`. Rows are never deleted. An addendum does not
change the row.

## Worked supersede

`examples/ADR-0002` chose self-hosted RabbitMQ as the message bus. When
multi-region deployment made a managed broker the better choice, the decision
changed in substance and `examples/ADR-0004` superseded it. ADR-0001, the
decision to use a message bus at all, is a separate decision and is untouched.
The old status line, the new ADR, and the index rows for 0002 and 0004 land in
one commit.

The old ADR keeps its body exactly as written. Only the status line changes:

```markdown
# ADR-0002 — Use RabbitMQ as the message bus

**Status:** Superseded by [ADR-0004](0004-use-azure-service-bus-as-the-message-bus.md) (2026-09-30)
```

The new ADR:

```markdown
# ADR-0004 — Use Azure Service Bus as the message bus

**Status:** Accepted (2026-09-30) · **Supersedes:** [ADR-0002](0002-use-rabbitmq-as-the-message-bus.md)
```

Its Context states what ADR-0002 decided and what changed to make a different
decision the right one.

## Worked addendum

`examples/ADR-0001` decided that services publish cross-service events to a
message bus. A duplicate-delivery incident later showed one of its consequences
in practice. The decision still reads true, so the incident and its cost are
recorded in a `## Addendum 2026-08-19` section at the end of ADR-0001.
Its status line and index row do not change.

## Worked rejection

`examples/ADR-0003` proposed a shared database across services. It keeps its
Context, Decision, and Consequences as proposed, takes `Rejected` on its status
line, and ends with a `## Rejection` section stating why and what is done
instead.

## Retrospective ADRs

An ADR written after the fact to document architecture as built meets the same
two tests as any other ADR. Its status is `Accepted (retrospective, YYYY-MM-DD)`,
dated the day it is written. Context states what was already in place and,
where known, when it was adopted. Record the alternatives and reasons where
they are known, and say so where they are not.
