# ADR format reference

A complete worked set lives in `examples/`: one ADR holding two decisions, the
two ADRs it split into, and the index that lists all three.

## Template

```markdown
# ADR-NNNN — Title stating the decision

**Status:** Proposed (YYYY-MM-DD)

## Context

The situation that forces a decision: the constraints that apply, what is
already true, what was measured. Enough for a reader years later to judge
whether those constraints still hold.

## Decision

What was decided, in the active voice. One bolded lead per decision when the
ADR carries more than one. Alternatives that were rejected go here, with the
reason they were rejected.

## Consequences

What follows from the decision — what becomes possible, what becomes harder,
what work it creates, what it forecloses. Both directions, not only the
favourable one.
```

## Header grammar

The status line is one line, fields separated by ` · `. `NNNN-slug.md` stands
for the target ADR's filename.

| Case | Status line |
|------|-------------|
| Proposed | `**Status:** Proposed (2026-06-18)` |
| Accepted | `**Status:** Accepted (2026-06-18)` |
| Accepted, supersedes in full | `**Status:** Accepted (2026-06-18) · **Supersedes:** [ADR-0001](NNNN-slug.md)` |
| Accepted, supersedes part | `**Status:** Accepted (2026-06-18) · **Supersedes:** part of [ADR-0001](NNNN-slug.md)` |
| Accepted, supersedes named items | `**Status:** Accepted (2026-06-18) · **Supersedes:** items 1 and 4 of [ADR-0001](NNNN-slug.md)` |
| Superseded | `**Status:** Superseded by [ADR-0002](NNNN-slug.md) (2026-06-18)` |
| Superseded by two | `**Status:** Superseded by [ADR-0002](NNNN-slug.md) (publishing) and [ADR-0003](NNNN-slug.md) (identity), 2026-06-18` |
| Deprecated | `**Status:** Deprecated (2026-06-18) — no longer applies; not replaced` |

The date is the date the status was reached, not the date of the edit.

Projects that track decisions against an issue tracker, epic, or ticket can add
a field of their own to this line using the same ` · ` separator. Nothing here
assumes one exists.

When a supersede is partial, the status line says which part. A bare
`Superseded by` on an ADR where only one of several decisions changed sends the
reader to an ADR that does not mention the rest.

## Index table

`README.md`, in the same directory as the ADRs — the full file is in
`examples/README.md`.

```markdown
## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-slug.md) | Title stating the decision | Superseded by ADR-0002 and ADR-0003 |
| [0002](0002-slug.md) | Title stating the decision | Accepted |
| [0003](0003-slug.md) | Title stating the decision | Accepted |
```

Superseded rows keep their number and title and carry the pointer in the Status
column. Rows are never deleted.

## Worked supersede

`examples/ADR-0001` held two independent decisions — the publishing trigger and
the publisher identity. When the identity decision changed, it was split rather
than edited. Three headers change or appear, and the index row for 0001 is
rewritten, all in one commit.

The old ADR keeps its body exactly as written. Only the status line changes:

```markdown
# ADR-0001 — Publish images on merge; least-privilege publisher identity

**Status:** Superseded by [ADR-0002](0002-publish-images-on-merge.md) (publishing) and [ADR-0003](0003-publisher-identity-federated-over-oidc.md) (identity), 2026-06-18
```

The ADR carrying the unchanged half forward:

```markdown
# ADR-0002 — Publish images on merge

**Status:** Accepted (2026-06-18) · **Supersedes:** part of [ADR-0001](0001-publish-images-on-merge-and-publisher-identity.md)
```

Its Context states that ADR-0001 held both decisions, that they are independent,
and that this ADR carries the publishing decision forward unchanged.

The ADR carrying the changed half:

```markdown
# ADR-0003 — Publisher identity federated over OIDC

**Status:** Accepted (2026-06-18) · **Supersedes:** part of [ADR-0001](0001-publish-images-on-merge-and-publisher-identity.md)
```

Its Context states what ADR-0001 decided, what went wrong with it, and what
changed to make a different decision available.

## Retrospective ADRs

An ADR written after the fact to document architecture as built takes
`**Status:** Accepted (retrospective — documents the architecture as built)`.
Context states what was already in place. There is no decision date to claim and
no alternatives to record.
