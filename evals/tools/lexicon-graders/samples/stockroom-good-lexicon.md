# Stockroom glossary

The words someone needs defined to talk about using or developing Stockroom.
A term belongs here if it is language rather than code, needs defining, and is
the one word for its concept. Keep entries in alphabetical order.

**adjustment** — A movement that corrects on-hand without any goods moving, posted after a count.

**allocation** — Assigning specific bins to a reserved order line. Distinct from a *reservation*, which names no bin.

**available** — The quantity of a SKU that can still be promised to a new order: its on-hand less everything reserved,
except quarantined units, which are on-hand but never available. A figure for the whole warehouse, not for a bin.

**backorder** — An order line accepted with nothing available to reserve. It has no *reservation*.

**batch** — The units of a SKU received together under one batch number. Not a batch job. The code calls it StockLot.

**bin** — The smallest addressable storage location in the warehouse.

**cycle count** — A count of some bins done without stopping picking. Distinct from a *stocktake*.

**movement** — A recorded change of stock from one bin to another bin.

**on-hand** — The units physically in a bin. "stock level" is not used.

**packing slip** — The document packed with an order, listing its lines and batches. "despatch note" is not used. (Rename awaiting sign-off.)

**pick queue** — The pick tasks waiting for pickers, ordered by wave and walk sequence. Not first-in-first-out, and not the job queue.

**reservation** — Quantity of a SKU set aside for an order line. Distinct from an *allocation*: it names no bin.

**reservation TTL** — How long a *reservation* holds before it lapses and its quantity is *available* again.

**return** — Goods a customer sends back.

**SKU** — A distinct product the warehouse stocks. "item code" is not used.

**stocktake** — A full count with picking stopped. Distinct from a *cycle count*.

**zone** — A named area of the warehouse grouping bins.
