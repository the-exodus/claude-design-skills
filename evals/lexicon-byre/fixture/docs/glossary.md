# Byre glossary

Started in March 2022 from the words on the whiteboard at the first planning day; since then an entry has been added with each pull request that introduced a name.
Gaps: none.
A term earns an entry when the team has given something a name, whether in the code or in a decision record.

---

**cow** — A female that has calved at least once. Before her first calving she is a *heifer*.

**days in lactation** — The number of days since a cow's most recent calving, counted only while she is in *lactation*; a dry cow has none.

**dry off** — To stop milking a cow at the end of her *lactation*, usually about two months before her next calving; also the event itself, with its date. `LactationService` records it and closes the lactation. It starts the *dry period*.

**dry period** — The span between a cow's *dry off* and her next calving, in which she is not milked. It is not the *dry off*, which is the event that starts it. The target length is set by `dry_period_days`, which defaults to 60. `LactationService` works out each cow's due dry-off date by counting the target length back from her expected calving date. *ListBuilder* puts her on the dry-off list seven days before that date. Because the expected calving date comes from her last service, a cow with no service on record never reaches the dry-off list and has to be dried off by hand. A cow whose dry period will be shorter than 40 days is marked as short on the calving list. The default was 56 days until release 2.3, when it was raised to 60 because cows calving a few days early kept falling inside the 54-day minimum of the dry cow tubes in use.

**Env** — The value passed as the first argument to every operation: the *farm*'s settings, the clock and the database handle. Nothing reads the time or a setting except through it.

**farm** — The dairy business whose herd Byre keeps the records for.

**GroupManager** — Moves animals between *management groups*, suggests the moves that follow a *dry off* or a calving, and keeps the history of every move.

**heifer** — See *cow*.

**HerdStore** — The store of animal records, keyed by ear tag. Every read and write of an animal goes through it.

**lactation** — The span in which a cow gives milk, from a calving to the following *dry off*. *ListBuilder* shows its *days in lactation* beside the cow on every list.

**lactation number** — The count of a cow's *lactations*, the first starting at her first calving; a cow in her third lactation has lactation number 3.

**late-reading rule** — A meter reading that arrives after its *session* has closed still belongs to the session in which it was taken, never to the one that is open when it arrives.

**ListBuilder** — Builds the daily lists: withhold, dry-off, calving, serve and cull. Each list is built afresh from the records every time it is asked for.

**management group** — A set of animals kept, fed and handled together, such as the milkers, the dry cows or the close-up cows. An animal is in exactly one management group at a time.

**MeterIngest** — Receives the readings from the parlour's milk meters and turns each one into a *milking*.

**milking** — One cow milked once, recorded with the time and the yield.

**parity** — The number of times a cow has calved. A *heifer* has parity 0.

**session** — One round of milking the whole herd; a *farm* has two or three a day. Not a *milking*, which is one cow's part in a session.

**user** — A person who uses Byre, such as the herd manager or a milker.

**VWP** — Voluntary waiting period: the number of days after calving during which a cow is deliberately not served, even if she is seen in heat. Set per *farm*.

**withdrawal period** — The time after a treatment during which produce from the treated animal may not be sold. A cow in a withdrawal period is always withheld from the bulk tank, and her milk is never counted as saleable until the period has ended.

**withhold sweep** — The pass that runs when a *session* opens and marks every cow with an open milk withdrawal, so that no *milking* of hers is counted towards the tank. Because of it, a cow under milk withdrawal is on the withhold list before the first cluster goes on.
