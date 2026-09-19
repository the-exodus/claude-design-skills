# Stockroom glossary

The words we need to talk about Stockroom, in one place. A word earns an
entry only if all three hold:

1. **It is language, not code.** A user meets it, or developers need it to
   talk about the system's behaviour across more than one part of the code
   and it would survive a rewrite with a different decomposition. Classes,
   modules, queues, jobs and other mechanisms are read in the code, and
   documented beside it.
2. **It needs defining.** Its ordinary meaning does not carry what it means
   here: it is overloaded, or narrower than ordinary use, or it names a
   distinction that must not be conflated.
3. **It is the one word for its concept.** Two words for one thing are one
   entry, under the word the domain uses, saying which word is not used.

Keep entries in alphabetical order. Consolidated 2026-09-20.

**adjustment** — A *movement* that corrects *on-hand* without any goods moving, posted after a count.

**allocation** — Assigning specific *bins*, and the *batches* in them, to a reserved order line. Distinct from a *reservation*, which sets quantity aside without naming any bin. To allocate is to make an allocation. See ADR-0001.

**available** — The quantity of a *SKU* that can still be promised to a new order: its *on-hand* less what open *reservations* hold against it, never counting units in a *quarantine* bin. A figure for the whole warehouse, not for a *bin*, because a reservation names no bin.

**backorder** — An order line accepted when too little is *available* to *reserve* it. It waits for the next *receipt*; unlike a *reservation*, it holds no quantity.

**batch** — The units of one *SKU* received together, sharing an expiry date and a batch number. Operators, labels and screens say batch; in the code the word already means a nightly job, so the code says lot. See ADR-0005.

**bin** — The smallest addressable storage location in the warehouse. Every unit *on-hand* is in exactly one bin. Operators sometimes say shelf; shelf is not used here.

**cycle count** — Counting a few *bins* while the warehouse carries on working around the counter. A *stocktake* closes the floor; a cycle count does not.

**movement** — A transfer of units of a *SKU* from one *bin* to another bin. Every change to *on-hand* is a movement.

**on-hand** — The units of a *SKU* physically in a *bin*, counted per bin. Quarantined units are on-hand. Operators call a SKU's on-hand its stock level.

**packing slip** — The document packed with a shipment, listing the *SKUs*, *batches* and quantities in it. Not called a despatch note.

**pick list** — The pick tasks handed to one picker for one wave in one *zone*.

**pick queue** — The released pick tasks waiting to be handed to pickers. Not first-in-first-out, despite the name: tasks come off it by wave, then by walk sequence through the *zone*.

**putaway** — Moving received units into *bins*.

**quarantine** — A *bin* held back from orders. Its units are *on-hand* but never *available*: they cannot be *reserved*, *allocated* or picked until someone has inspected them.

**receipt** — Goods arriving into the warehouse, recorded at goods-in before *putaway*.

**reservation** — A quantity of a *SKU* set aside for an order line, not tied to any *bin*. Distinct from an *allocation*, which names the bins. A reservation lapses after a time operators set, and its quantity is *available* again at once. See ADR-0001.

**return** — Goods a customer sends back against an order. They arrive as a *receipt*, into a *quarantine* bin, until someone has inspected them.

**SKU** — Stock-keeping unit: one sellable product variant, such as one size and colour of a product, tracked as its own line of stock. Identified by its code; item code is not used.

**stocktake** — A count of every *bin* in the warehouse, taken with all picking stopped. Distinct from a *cycle count*.

**zone** — An area of the warehouse with its own pickers.
