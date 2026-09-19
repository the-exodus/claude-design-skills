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

A term earns an entry only by passing all three. Apply test 1, then check
whether the word is a synonym of a surviving entry (test 3's first rule), then
test 2, then the rest of test 3. The first test it fails decides its verdict.

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

Fails this test: a module, class, component, service, layer, thread, queue,
file, data structure, or the name of a mechanism inside the build — including a
word that spans several parts only because the build is cut the way it is, such
as a hand-off between two components. The behaviour such a word names goes to
the concept it serves, usually a case of an existing entry, or to the decision
records. Also fails: the project's working vocabulary — its test doubles,
harnesses, tools and process — which belongs in its conventions.

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

- **It is overloaded**: someone using or developing the system would plausibly
  apply another sense of the word to the same things — another sense in the
  system, a platform class or message name a user meets, a data structure a
  developer would expect behind the word (a *queue* that is not FIFO). A
  collision the project itself records also counts: a decision record, a
  convention, or a component named to dodge the word. An incidental
  programming-language sense does not: a function's return value is no
  overload of returning a parcel.
- **It is narrower than ordinary use.** "Pending means submitted and not yet
  reviewed" — the domain fixed what the word covers. A word whose boundary the
  system fixes is narrower even when the word is everyday: *business day* in a
  payments system, where the system decides which days count.
- **It names a distinction that must not be conflated.** Near-synonyms that
  must never be used for each other: archive vs. delete, user vs. member,
  refund vs. reversal. These are the highest-value entries.

Fails this test: a word used in its ordinary sense, however central it is. Also a
word whose only specific content is a decision about how the thing behaves —
that is a decision record's content. For example, *invoice* in a billing
system: the ordinary sense covers it, and that invoices are numbered per year is
a decision, so it fails — unless the system distinguishes it from something a
reader would also call an invoice, such as a *credit note*; then the entry exists
for that distinction and names it.

### 3. It is the one word for its concept

Two entries for one concept are one entry. Merge them under the word the domain
uses, and say in that entry which word is not used. Shades of one concept are not
separate terms unless the difference must be preserved, in which case test 2
already holds for both and each entry names the other.

- **Check for synonymy before retiring a word under test 2.** A synonym of a
  surviving entry is a merge, recorded there as a word not used, even if it would
  also fail test 2 — otherwise nothing tells a reader it is not used.
- **A redirect** ("see *X*") is either a synonym, merged into *X*, or — if the
  word passes tests 1 and 2 — a distinct term missing its entry, rewritten into
  one.
- **A headword the sources don't use** is drift. If the code and every reference
  agree on one other word, write the entry under their word, record the old one
  as not used, and mark the rename for sign-off. If they disagree among
  themselves, keep the headword and surface the split.

## An entry

```markdown
**term** — What it means, in the domain's words. Distinct from *other term*,
which ... See [ADR-NNNN](...).
```

- **What the term means**, in one to three sentences, in words a user or a new
  developer already has.
- **What it is distinct from**, naming the other term, when the distinction is
  why the entry exists — including any overload (test 2) the entry doesn't yet
  state.
- **At most one pointer**, to the decision record whose decision defines what
  the word means; where that part of it has been superseded, the superseding
  record. Not every record that touched the concept.
- Other lexicon terms are italicized where used. Only terms the lexicon defines.

Not in an entry:

- How it is implemented: threads, types, API calls, which component does what.
- How it behaves, its edge cases, and what happens when: the decision records,
  the references and the tests carry that. Except a clause that distinguishes
  the term from a near-synonym — an archived item can be restored, a deleted one
  cannot — which is meaning even when it reads as behaviour. Keep it.
- Configuration keys, verbs and their arguments: the references.
- Ticket numbers, and the history of how the meaning came about.

To tell meaning from behaviour: a clause that says how the term differs from a
neighbouring term is meaning. For any other clause, ask whether the word would
still pick out the same things if the clause were false; if so, it is
behaviour.

When you cut a condition or an exception, cut or qualify the universal it
qualified. Never leave *every*, *never* or *only* standing without its
exception.

An entry past about fifty words is almost always carrying code or a decision.

**An entry changes only when the meaning changes.** A new decision about the
concept goes into a decision record, and the entry is untouched unless that
decision changed what the word means.

## Size

A domain's language usually comes to twenty or thirty terms. That is a symptom
check, not a quota: past it, the lexicon is probably admitting code or
decisions. Don't cut an entry that passes the tests to reach a number, and don't
keep one that fails them because there is room. A system that users meet through
several surfaces can honestly sit above thirty; say so rather than cutting
further.

## Consolidating a lexicon

A lexicon accumulates and drifts however strictly entries are admitted. This is
the procedure for bringing one back. It changes the lexicon and nothing else.

1. **Read the lexicon in full**, then index where displaced content could live:
   the decision records, the project's references, conventions, README and any
   architecture overview, the tests, the code for any name an entry describes,
   and the code's doc comments. Note the commit or date you audit, and cite
   evidence at it.

2. **Test every entry, in order.** For each, record a verdict, the test that
   decided it, and one line of reason:

   - **retire** — fails test 1 or test 2, and nothing behind it needs a word of
     its own. Say where the word belongs instead: the type or module it names,
     the conventions, the existing entry that already carries the concept, or
     nowhere.
   - **reframe** — fails test 1, but the concept or guarantee behind it needs a
     word the lexicon doesn't yet give it. If an existing entry is that word,
     name it and carry over only meaning and distinction. Otherwise write a new
     entry under the word the user documentation or the code already uses, and
     list it in step 6 as a new entry awaiting sign-off — not also as a gap. An
     entry for a component that exists, or was named, to avoid a domain word is
     a reframe to that word.
   - **merge** — fails test 3. Name the entry it merges into.
   - **rename** — passes, but under a headword the sources don't use (test 3).
     Name the new headword; it awaits sign-off.
   - **rewrite** — passes, but is not in the shape above. Reduce it to meaning
     and distinction, adding any overload it doesn't state, with where each
     sense is met. Don't define a second term inside the entry where the sources
     use that term differently; that is drift.
   - **keep** — passes, is already in shape, names no component, and has no
     unstated overload. Adding italics, or a "not used" note from a merge, does
     not make a keep a rewrite.

   Judge the term, not its current definition. A word that belongs can have an
   entry that has turned into a description of code; that is a rewrite, not a
   retirement.

3. **Correct.** Check every claim the shaped entries make against how the code
   and the references use the word. Compare what is being cut with the home step
   4 finds for it, and report a disagreement there as drift too.
   - Where the code or the references split the term into cases — an enum, a
     reported value, a kind of rule, a configuration option, a class of
     trigger — check every claim against every case. A case the claim does not
     fit is drift, not a finer grain.
   - Check every universal — *only*, *never*, *always*, *every*, *all*, *none*,
     *cannot*, *entirely*, and the like — against each reference that mentions
     the word.

   Surface each disagreement with its evidence, `file:line` as a search of the
   file reports it — a citation that does not open to the quoted text is not
   evidence — and let the user say which side is right. Don't settle it by
   rewriting either side.
   - A disputed claim that is the entry's meaning or distinction stays in the
     entry, unchanged in substance, until the user answers — in words that
     survive, never in a word retired under test 1 or merged as not used. A word
     retired under test 2 is ordinary and free to use.
   - A disputed claim about behaviour is not carried into the entry. Quote it in
     the drift finding, name the sources on each side, and account for it in
     step 4. Cutting it settles nothing: the lexicon simply no longer asserts it.

4. **Account for everything cut**, entry by entry: where the removed content
   already lives. Search the decision records, README, tests and doc comments
   for the sentence's substance, not its wording, before calling anything
   homeless. List sentence by sentence only what has no other home: each is a
   missing decision record, a missing doc comment or convention, or something
   nobody needs. Cutting an entry must never be how a decision disappears. Don't
   write the content elsewhere yourself.

5. **Fix the edges.**
   - **Inside the lexicon:** cross-references to entries that were retired or
     merged. Fix them.
   - **Outside it:** code comments that cite the lexicon for a retired word or
     define a surviving one through a retired one, and references and decision
     records that use a retired word as if it were defined; and any convention
     that tells people to add a lexicon entry for a code name. List them; don't
     edit them.
   - **Gaps:** a word the surviving entries or the references use in a
     narrower sense than ordinary without defining it, which the audit turned
     up — and a domain word some component was named to avoid. Propose these;
     don't brainstorm. Where the file has no gaps line, present them only.

6. **Present, then write.** Show:
   - entries and words, before and after;
   - the verdicts, grouped by verdict, with the test that decided each, and
     any new entries and renames awaiting sign-off;
   - the homeless content, the drift findings, the outside edges and the
     proposed gaps;
   - the consolidated lexicon in full.

   The lexicon is shared vocabulary, so the user signs off before anything is
   written. Then write it where it was:
   - Keep its ordering and link style.
   - Replace any statement in its header of what earns an entry or how entries
     were admitted — including provenance or inference lines that give
     admission reasons — with the three tests.
   - A standing exclusion in the header (a class of words said to belong
     elsewhere) goes too. Re-test the excluded words the surviving entries use,
     and propose those that pass as gaps.
   - Put proposed gaps on the file's gaps line, if it has one, marked as not yet
     admitted; a gap becomes an entry only when the user admits it.
   - Update any provenance line to say it was consolidated, and when, and drop
     retired terms from it.
