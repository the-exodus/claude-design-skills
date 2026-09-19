---
name: lexicon
description: >
  House rules for a project's lexicon — the domain's ubiquitous language — and
  the procedure for pruning, consolidating and correcting one that has sprawled.
  Load before admitting, amending or retiring a lexicon or glossary entry in any
  repo; when asked to review, audit, prune, consolidate, clean up or correct a
  lexicon or glossary; and when a lexicon has grown past about thirty entries or
  its entries describe code rather than meaning. design-interview loads it for
  the admission tests. NOT for API reference documentation, code doc comments,
  or user manuals.
---

# Lexicon

A lexicon holds the words someone needs defined to talk about using or
developing the system — the domain's language, in the DDD sense. It exists so
that two people, or two documents, cannot mean different things by the same
word.

**The code takes its names from the lexicon, never the other way round.** A
module, a class, a thread or a mechanism is part of the code, and the code is
what you read to talk about it; its documentation lives beside it. A lexicon that
admits the code's parts turns into a second, drifting description of the code,
and stops being read.

## Location

The lexicon lives wherever the project already keeps it. Scan for it:

- `docs/lexicon.md`, `docs/design/lexicon.md`
- `docs/glossary.md`, `GLOSSARY.md`, `LEXICON.md`
- `.claude/lexicon.md`

Where none exists and one is needed, ask where it goes, with a concrete
suggestion drawn from where the project keeps its other design documentation.

## The tests

A term earns an entry only by passing all three, in order. The first test it
fails decides its verdict, so apply them in this order and stop at the first
failure.

### 1. It is language, not code

**Does someone need the word to talk about what the system does, without
pointing at a particular part of the code?** It is language if either holds:

- **A user meets it** — in the user documentation, the configuration, the
  commands, the messages, the output — unless what the user meets is a
  mechanism's name; then the third case below decides.
- **Developers need it to talk about the system's behaviour across more than one
  part of the code, and it would survive a rewrite of the code with a different
  decomposition** — a concept the whole design is reasoned in, such as
  *settlement* in a payments system.

A word used only inside one part of the code, and in the decision records about
that part, is code, however carefully a decision record defined it. The record
defines it in its own text; the lexicon does not repeat it.

Fails this test: a module, class, component, service, layer, thread, queue,
file, data structure, or the name of a mechanism inside the build. Also the
project's working vocabulary — its test doubles, harnesses, tools and process —
which belongs in the project's conventions, not its domain language.

A word that spans several parts only because the build is cut the way it is — a
hand-off between two components, a unit of work one component batches for
another — fails. The behaviour it names goes to the concept it serves, usually a
case of an existing entry, or to the decision records.

Three cases need care:

- **A concept and the component that realizes it.** An order's *fulfilment* is a
  concept anyone talking about a shop needs, however the code is cut; the
  `FulfilmentService` that performs it is code. Keep the concept, not the
  component.
- **A mechanism and the guarantee it serves.** A user relies on "a cancelled
  order is never charged", not on the job that voids the charges. If the
  guarantee needs a word, the entry is the guarantee's, under the domain's word
  for it. The mechanism's name stays in the code.
- **A mechanism's name the user documentation already uses.** Documentation
  that tells users about "the retry worker" is still telling them about a
  routine. The entry is for what the user observes — a delivery that was
  *retried* — if that needs a word at all, and the documentation's use of the
  mechanism's name is drift to surface.

### 2. It needs defining

**Does the word mean something here that its ordinary meaning does not carry?**
At least one must hold:

- **It is overloaded.** The same word means different things in different parts
  of the system, or the domain's meaning differs from the ordinary one.
- **It is narrower than ordinary use.** "Pending means submitted and not yet
  reviewed" — the domain fixed what the word covers.
- **It names a distinction that must not be conflated.** Near-synonyms that
  must never be used for each other: archive vs. delete, user vs. member,
  refund vs. reversal. These are the highest-value entries.

Fails this test: a word used in its ordinary sense, however central it is. Also a
word whose only specific content is a decision about how the thing behaves —
that is an ADR's content, and a decision having been made about something is not
a reason for its name to be defined.

### 3. It is the one word for its concept

Two entries for one concept are one entry. Merge them under the word the domain
uses, and say in that entry which word is not used. Shades of one concept are not
separate terms unless the difference between them must be preserved, in which
case test 2 already holds for both and each entry names the other.

An entry that only redirects to another ("see *X*") is one of two things: a
synonym, merged into *X* as a word not used, or a distinct term missing its
entry, which is rewritten into one.

Check for synonymy before retiring a word under test 2. A word that is a synonym
of a surviving entry is a merge, recorded in that entry as a word not used, even
if it would also fail test 2 — otherwise nothing tells a reader it is not used.

A headword that names a part of the code — a module, a class, a layer — fails
test 1 and is reframed to the documentation's word for the concept. A headword
that differs from the word the code and the documentation use, neither being a
part of the code, is drift, not a merge: surface it, don't pick.

## An entry

```markdown
**term** — What it means, in the domain's words. Distinct from *other term*,
which ... See [ADR-NNNN](...).
```

- **What the term means**, in one to three sentences, in words a user or a new
  developer already has.
- **What it is distinct from**, naming the other term, when the distinction is
  why the entry exists.
- **At most one pointer**, to the decision record whose decision defines what
  the word means, if one does; where that part of it has been superseded, the
  superseding record. Not every record that touched the concept.
- Other lexicon terms are italicized where used. Only terms the lexicon defines.

Not in an entry:

- How it is implemented: threads, types, API calls, the order of calls, which
  component does what.
- How it behaves, its edge cases, and what happens when: the decision records,
  the references and the tests carry that. The one exception is a behavioural
  clause that *is* the distinction — an archived item can be restored, a deleted
  one cannot. Keep that clause; it is the meaning. Cut the rest.
- Configuration keys, verbs and their arguments: the references.
- Ticket numbers, and the history of how the meaning came about.

An entry that needs any of these to be understood is describing code (test 1) or
a decision (an ADR). An entry past about fifty words is almost always carrying
one of them.

**An entry changes only when the meaning changes.** A new decision about the
concept goes into a decision record, and the entry is untouched unless that
decision changed what the word means. This is what keeps entries from growing a
sentence with every decision that touches them.

## Size

A domain's language usually comes to twenty or thirty terms. That is a symptom
check, not a quota: past it, the lexicon is probably admitting code or
decisions, and it needs consolidating. Don't cut an entry that passes the tests
to reach a number, and don't keep one that fails them because there is room. A
system that users meet through several surfaces can honestly sit above thirty;
say so rather than cutting further.

## Consolidating a lexicon

A lexicon accumulates and drifts however strictly entries are admitted. This is
the procedure for bringing one back. It changes the lexicon and nothing else.

1. **Read the lexicon in full**, then index where displaced content could live:
   the decision records, the project's references, conventions, README and any
   architecture overview, the code for any name an entry describes, and the
   code's doc comments. Note the commit or date you audit, and cite evidence at
   it: a project that moves while you work moves your citations with it.

2. **Test every entry, in order.** For each, record a verdict, the test that
   decided it, and one line of reason:

   - **retire** — fails test 1 or test 2, and nothing behind it needs a word.
     Say where the word belongs instead: the type or module it names, the
     conventions, or nowhere.
   - **reframe** — fails test 1, but the concept or guarantee behind it needs a
     word. If that concept already has an entry, name it; the reframed entry
     carries over only meaning and distinction. If it has none, write a new
     entry under the word the user documentation or the code already uses for
     it, and list it in step 6 as a new entry awaiting sign-off — not also as a
     gap.
   - **merge** — fails test 3. Name the entry it merges into.
   - **rewrite** — passes, but is not in the shape above. Reduce it to meaning
     and distinction. Where the word is overloaded — against another sense in
     the system, or on the platform — and the entry doesn't say so, add that
     distinction: it is the entry's reason to exist. Add it only when someone
     talking about using or developing the system meets both senses — in the
     user documentation, the configuration or the output, or in the platform API
     the system is built on — and cite where. A programming-language sense (a
     function's return value, a field named after the word) or a platform term
     the project's user-facing text never uses is not an overload. Where the
     sources disagree about which sense holds, that is drift for step 3, not a
     distinction to add. Don't define a second term inside the entry where the
     sources use that term differently; that is drift too.
   - **keep** — passes, is already in shape, names no component, and has no
     unstated overload.

   Judge the term, not its current definition. A word that belongs can have an
   entry that has turned into a description of code; that is a rewrite, not a
   retirement.

3. **Correct.** Check every claim the original entries made, and what the
   shaped entries still say — including those a reframe created or fed —
   against how the code and the references use the word.
   - Where the code or the references split the term into cases — an enum, a
     reported value, a kind of rule, a configuration option or backend, a class
     of trigger — check every claim in the entry against every case. A case the
     claim does not fit is drift, not a finer grain.
   - Check every universal in the entry — *only*, *never*, *always*, *every*,
     *all*, *none*, *cannot*, *entirely*, and the like — against each reference
     that mentions the word. Each is a claim.

   Surface each disagreement with its evidence, `file:line` as a search of the
   file reports it — a citation that does not open to the quoted text is not
   evidence — and let the user say which side is right. Don't settle it by
   rewriting either side.
   - A disputed claim that is the entry's meaning or distinction stays in the
     entry, unchanged in substance, until the user answers — stated in words
     that survive, never in a word retired under test 1 or merged as not used.
     A word retired under test 2 is ordinary and free to use in its ordinary
     sense.
   - A disputed claim about how the thing behaves is not carried back into the
     entry. Quote it in the drift finding, name the sources on each side, and
     account for it in step 4 like any cut sentence. Cutting it settles nothing:
     the lexicon simply no longer asserts it.

4. **Account for everything cut**, entry by entry: where the removed content
   already lives — a decision record, a reference, a test, a doc comment. Search
   the doc comments before calling anything homeless. Then list, sentence by
   sentence, what has no other home: each is a missing decision record, a
   missing doc comment, or something nobody needs. Cutting an entry must never
   be how a decision disappears. Don't write the content elsewhere yourself.

5. **Fix the edges.**
   - **Inside the lexicon:** cross-references to entries that were retired or
     merged. Fix them.
   - **Outside it:** code comments that cite the lexicon for a retired word, and
     references and decision records that use a retired word as if it were
     defined. List them for the user; don't edit them.
   - **Gaps the audit turned up:** a word the surviving entries or the
     references use in a narrower sense than ordinary without defining it. A
     component's name that exists only to avoid a domain word is the usual
     sign: the domain word is a reframe (step 2) if the component had an
     entry, a gap if it did not. Propose these; don't brainstorm terms the
     audit did not turn up.

6. **Present, then write.** Show:
   - entries and words, before and after;
   - the verdicts, grouped by verdict, with the test that decided each, and
     any new entries a reframe created;
   - the homeless content, the drift findings, the outside edges and the
     proposed gap entries;
   - the consolidated lexicon in full.

   The lexicon is shared vocabulary, so the user signs off before anything is
   written. Then write it where it was:
   - Keep its ordering and link style.
   - Replace any statement in its header of what earns an entry, or of how
     entries were admitted — including provenance or inference lines that give
     admission reasons — with the three tests. That includes any standing exclusion — a class of words said to
     belong elsewhere: re-test the excluded words the surviving entries use, and
     propose those that pass as gaps.
   - Put proposed gaps on the file's gaps line, if it has one, marked as not yet
     admitted; a gap becomes an entry only when the user admits it.
   - Update any provenance line to say it was consolidated, and when, and drop
     retired terms from it.

## Anti-patterns

- Admitting a word because the code has a type by that name. The type takes its
  name from the lexicon, or from nobody.
- Adding a sentence to an entry because a decision touched the concept.
- Defining a term by what the code does with it.
- Keeping an entry because it is used a lot. Frequency is not test 2.
- Retiring a term because its definition is bad. Fix the definition.
- Consolidating to a number instead of by the tests.
