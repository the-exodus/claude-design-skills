---
name: adr
description: >
  House rules and format for Architecture Decision Records. Load
  before writing, reviewing, superseding, or indexing an ADR in any repo, and
  when asked to record a decision, write something up as an ADR, add to or
  reindex a directory of ADRs, or change an ADR's Status. Also load when a
  decision already recorded in an ADR has changed, since ADRs are superseded
  rather than edited. NOT for architecture pages on the wiki, RFCs, or design
  docs that record no decision.
---

# Architecture Decision Records

One format, applied in every repo — including ones whose existing ADRs have
drifted from it. Those stand as valid historical records; they are not converted
in bulk, and they are not reference material. Write new ADRs to this format.

Superseding an old ADR does mean editing it — that is the one edit an old ADR
gets. Record the new status in the field that ADR already uses, whether that is
a `**Status:**` line, a bare `Status:` line, or a `## Status` section. Where it
carries no status at all, add the `**Status:**` line from this format. Leave the
body alone either way.

`references/format.md` carries the template, the header grammar, and a worked
supersede.

## Location and index

ADRs live wherever the project already keeps them. Scan for the directory:

- `docs/adr/`, `docs/adrs/`
- `docs/architecture/decisions/`, `docs/decisions/`
- `architecture/decisions/`, `architecture/adr/`
- `adr/`, `adrs/`

Write into whichever exists. Where several do, use the one holding the most ADRs
and say which you picked. Where none does, ask — with a concrete suggestion
drawn from what the repo actually looks like, a `docs/` that already exists or
its ecosystem's convention. Don't pick silently, and don't create a directory
this skill preferred.

Files are `NNNN-kebab-case-title.md`, numbered sequentially from `0001` — take
the highest number present and add one. If two ADRs land on the same number,
renumber the later one and fix its links.

`README.md` in that same directory holds the canonical index table. Where a repo
has none, write it, listing every ADR already there.

The index is part of the change. Adding an ADR or changing a Status updates the
table in the same commit.

## Format

Michael Nygard's lightweight format — Context / Decision / Consequences, with a
Status.

```markdown
# ADR-NNNN — Title stating the decision

**Status:** Accepted (YYYY-MM-DD)

## Context
## Decision
## Consequences
```

Status is one of: `Proposed`, `Accepted`, `Deprecated`, `Superseded`.

The title states the decision, not the topic: "Reconcile with Terraform on a
timer", not "Reconciliation approach".

## Supersede, never update

An ADR is not edited when its decision changes. Write a new ADR and mark the old
one:

- Old ADR: record `Superseded by [ADR-NNNN](NNNN-slug.md) (YYYY-MM-DD)` in the
  status field it already has, naming the specific items when only part of it
  changed.
- New ADR: `**Supersedes:** [ADR-NNNN](NNNN-slug.md)`, or `part of
  [ADR-NNNN](NNNN-slug.md)` for a partial supersede.

A dated `Update YYYY-MM-DD` section appended to a standing ADR is wrong for a
decision change. An ADR is also not updated when its decision gets implemented —
implementation is tracked wherever the project tracks work.

## Splitting

Split an ADR when something actually pushes on it: one of its decisions is being
superseded, or the decisions have diverged in ownership or lifecycle. Do the
splitting inside the supersede that prompted it.

Do not decompose an ADR because a future split is imaginable. A hypothetical
("if the provider ever ships X, this half reverses") is not a case.

`references/examples/` is the model. ADR-0001 there held two separable
decisions — when images are published, and the identity that publishes them —
and was correctly written as one. It split into ADR-0002 and ADR-0003 at the
moment the identity decision actually changed, as part of writing that
supersede.

## Writing

Write for someone reading this years later to decide whether the decision still
holds. They need the constraints that applied, the decision taken, and what it
costs. Every sentence carries one of those.

ADRs are the format most likely to break that, because Context / Decision /
Consequences asks for reasoning. Alternatives considered, constraints, and the
reasons behind a decision are the ADR's content — record them. What to cut is
the framing around them:

- No scene-setting opener ("live verification killed it").
- No sentence that restates the previous one with more weight.
- No antithesis for emphasis ("the codec was not at fault — the design was").
- No list of three where only one item is load-bearing.

State a thing once, then move to the next or stop. Do not close a section by
restating it.
