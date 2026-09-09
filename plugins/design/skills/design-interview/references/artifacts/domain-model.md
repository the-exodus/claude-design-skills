# Domain Model

## What it's for

The concepts the system works with, what must be true of them, and the shapes they take at each boundary they cross.

Required when *the same concept has more than one shape*, *state outlives a single version*, or *it holds data that belongs to someone else* held at seeding.

## Scope note

Not a database schema, though a schema may be one of its outputs. Not a class diagram, and not tied to objects — a design in a language with records, maps, or algebraic types has a domain model exactly as much as one with classes.

Naming the concepts is the lexicon's job. This artifact says what is *true* of them. If you find yourself defining a term here, it belongs in the lexicon and its absence there is a gap.

## Must contain

**The concepts, and what distinguishes them.** For each: what identifies it, whether that identifier is assigned by the system or supplied by a caller, and whether it is stable for the concept's whole life.

Separate the concepts that *have* identity from those defined entirely by their values. It is not a formality — equality, sharing, and mutation all behave differently, and conflating the two is where aliasing bugs come from. Two amounts of the same currency are interchangeable; two accounts with the same balance are not.

**Relationships**, with cardinality stated in both directions. Which side owns the relationship. Whether it's optional. What happens to one side when the other is removed. And which relationships are structural — the child cannot exist without the parent — versus which are references between things that live independently. That distinction decides cascade behavior, and leaving it implicit is how orphans and accidental deletions both happen.

**Invariants — and where each one is enforced.** The second half is the part that's usually missing and the part that matters. An invariant can live:

- in the type, so an illegal instance can't be constructed
- in a constructor or factory, so it holds from creation
- in a boundary validator, so it holds for anything entering
- in the storage engine, as a constraint
- nowhere, in which case it is a hope rather than an invariant

Pick one per invariant and say which. Enforced in four places, it drifts; enforced nowhere, it is documentation of an intention. Also note which invariants hold at rest and which only hold at particular moments, since "always true except mid-transaction" is a different contract.

**Representations.** The section that usually doesn't exist, and the reason this artifact is worth writing:

- Every shape a concept takes — in-memory type, serialized payload, stored record, wire or API resource, config.
- **Which one is authoritative.** When two disagree, this is the answer, and without it there isn't one.
- Where the mapping between shapes lives, and whether it is mechanical or lossy. A lossy mapping is a design decision; say what's lost.
- What a field means when it is required in one shape and absent in another. Absent, null, and empty are usually three things.
- Whether identity survives a round trip.
- Which shapes are versioned independently. Two shapes that must change together are one shape with extra steps; two that can change apart need separate evolution rules.

**Notation over prose**, wherever a notation fits — DDL, JSON Schema, protobuf, type definitions, a resource schema. Prose domain models are where implementers most reliably diverge from intent, because prose can be internally consistent and still ambiguous.

## Completeness test

**A reader can construct a valid instance of every concept, and can say what would make one invalid, without asking you.**

And, per boundary: **they can say what a round trip through it preserves and what it loses.**

Anything not answerable is a gap to report, not a detail to settle here alone.

## Common failures

- **Modeling the storage and calling it the domain.** The persisted shape is one representation, and letting it be the model is how database concerns end up in every layer.
- **One shape everywhere.** Cheap and clean until the first time the wire format needs to change independently of storage, at which point it is the most expensive thing in the codebase.
- **A shape per layer with no stated authority.** Four representations and no answer to which is right when they disagree is worse than one shape, because it looks like it was designed.
- **Invariants without a location.** "Must be non-empty" is not a decision until it says where it's checked.
- **Conflating identity-bearing concepts with value concepts.** Different equality, different sharing rules, different bugs.
- **Prose where a schema would do.**
- **Coining a term here.** Names come from the lexicon. A concept the model needs and the lexicon doesn't have is a gap in the interview.
