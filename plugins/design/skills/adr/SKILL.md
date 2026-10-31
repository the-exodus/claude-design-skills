---
name: adr
description: >
  House rules and format for Architecture Decision Records. Load
  before writing, reviewing, superseding, or indexing an ADR in any repo, and
  when asked to record a decision, write something up as an ADR, add to or
  reindex a directory of ADRs, or change an ADR's Status. Also load when
  deciding whether a decision warrants an ADR at all, and when something about
  a decision already recorded in an ADR has changed, to decide between a
  superseding ADR and an addendum. NOT for architecture pages on the wiki,
  RFCs, or design docs that record no decision.
---

# Architecture Decision Records

One format, applied in every repo. Every new ADR follows it, including in repos
whose existing ADRs follow another format.

Existing ADRs in another format stand as valid historical records. They are not
converted, split, or re-judged against the rules below, and they are not
reference material. When a new ADR supersedes a decision recorded in one, the
one edit it gets is to its status, in the field it already uses: a
`**Status:**` line, a bare `Status:` line, or a `## Status` section. Superseded
replaces the status that was there; `Accepted` does not stay beside it. Where it
carries no status at all, add the `**Status:**` line from this format. Leave the
body alone either way.

Only where the existing ADR records other decisions that still stand does it
keep its status, and the supersede names the decision on both sides:

- Existing ADR: add `partly superseded by [ADR-NNNN](NNNN-slug.md)
  (<decision>, YYYY-MM-DD)` to its status field. Its index row reads
  `<its status>; partly superseded by ADR-NNNN`.
- New ADR: `**Supersedes:** the <decision> decision in
  [ADR-NNNN](NNNN-slug.md)` on its status line.

`references/format.md` carries the template, the header grammar, and worked
examples of a supersede, an addendum, and a rejection.

## What gets an ADR

A decision gets an ADR when it passes both tests:

- **Architecturally significant.** It affects the system's structure, its
  non-functional characteristics, its dependencies, its interfaces, or its
  construction techniques.
- **Hard to change later.** Reversing it means migrating data, breaking a
  contract that other services, teams, or customers depend on, or rewriting
  code across services.

Judge both at the time of the decision.

When asked to record a decision that fails either test, say which test it fails
and suggest where its reasoning belongs instead: the commit message, the PR
description, or a comment beside the code it explains. Write the ADR only if the
person still wants one.

## One decision per ADR

Each ADR records one decision. Two decisions are separate when either could be
overturned while the other stands; they get one ADR each, even when they are
taken together. The rejected alternatives to a decision belong in its ADR.

## Boundaries

A decision draws a boundary when a structural rule could see what it decided:
one module's use of another, a surface and the consumers allowed to use it, or
a prohibition. Most dependencies were never decided by anyone and are not
boundaries; a boundary is one a decision drew. How fine-grained a boundary is
(a package, a namespace, a project) is for the project's architecture tests to
say.

When an architecture test protects the boundary a record decides, the
Decision ends with this sentence, exactly:

> The architecture tests enforce this boundary.

Write it when the test exists, and when the test was decided together with
the boundary, as a design records it, even though the build has not written it
yet: the record and the test then ship together. A boundary nobody decided a
test for gets no sentence; if one is added later, the sentence goes in an
addendum then.

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

The title states the decision: "Reconcile with Terraform on a timer", not
"Reconciliation approach".

Status is one of:

- `Proposed` — under review. The body is edited freely until the decision is
  taken.
- `Accepted` — the decision is taken. The body is fixed from here; later changes
  follow [Supersede or addendum](#supersede-or-addendum).
- `Rejected` — the proposal was turned down. The body stays as proposed, and an
  appended `## Rejection` section states why.
- `Deprecated` — the decision no longer applies and nothing replaces it.
- `Superseded` — a later ADR replaced the decision.

## Supersede or addendum

Once an ADR is Accepted, its body is never rewritten. What changed decides how
the change is recorded.

**Supersede** when the decision is overturned or changes in substance: the
Decision section would have to be reworded to stay true. Narrowing or widening
the decision's scope is a change in substance. Write a new ADR and mark the old
one:

- Old ADR: `Superseded by [ADR-NNNN](NNNN-slug.md) (YYYY-MM-DD)` replaces its
  status, in the status field it already has. The field reads that and nothing
  else: not `Accepted. Superseded by …`.
- New ADR: a `**Supersedes:**` field on its status line, after a ` · `, not on
  a line of its own. Its Context states what the old ADR decided and what
  changed.

  ```markdown
  **Status:** Accepted (YYYY-MM-DD) · **Supersedes:** [ADR-NNNN](NNNN-slug.md)
  ```

**Append an addendum** when the Decision section still reads true: new context,
a consequence that has materialised, a measurement, a related ADR. Add a dated
`## Addendum YYYY-MM-DD` section at the end of the ADR. The existing text, the
status, and the index row stay as they are.

Only Accepted ADRs in this format take addenda. ADRs in another format get no
edit beyond their status. New information about a superseded decision goes in
the ADR that superseded it. Rejected and Deprecated ADRs are closed records.

A consequence serious enough to call the decision into question goes in an
addendum until a new decision is taken; that decision then supersedes.

An ADR is not updated when its decision gets implemented — implementation is
tracked wherever the project tracks work.

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

## Constraint

The ADR set is the history of how the architecture came to be, and the record
a reviewer or auditor checks decisions against. A decision edited in place
loses that history.
