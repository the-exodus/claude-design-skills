# Stockroom glossary

Every name used in Stockroom, in one place. A term belongs here if it
appears in the code, or a decision introduced it. Keep entries in
alphabetical order.

**adjustment** — A movement that corrects on-hand without any goods moving, posted after a count.

**allocation** — Assigning specific bins, and the lots in them, to a reserved order line, so a picker knows where to go. Distinct from a *reservation*, which sets quantity aside without naming any bin. To allocate is to make an allocation.

**AllocationEngine** — The class that performs allocation. It walks the bins for a SKU earliest-expiry first and skips quarantine bins. Lives in `stockroom/allocation.py`.

**available** — The quantity of a SKU that can still be promised to a new order: its on-hand less everything reserved against it, except for quarantined units, which are on-hand but never available. Available is a figure for the whole warehouse, not for a bin, because a reservation names no bin. `available_qty()` works it out by summing the bin rows and subtracting open reservations in a single query. It is computed on read rather than stored, as decided in ADR-0002 after the stored counter went stale during the 2024 peak. The API returns it as the `available` field of the SKU resource. Sales staff should treat anything below five as "call the warehouse" rather than promising a delivery date. When a reservation lapses, its quantity is available again at once.

**backorder** — See *reservation*.

**bin** — The smallest addressable storage location in the warehouse. Every unit on hand is in exactly one bin.

**box** — A cardboard box an order is shipped in.

**cycle count** — A count of one bin at a time, done without stopping picking. Distinct from a *stocktake*.

**despatch note** — The document packed with a shipment, listing the SKUs, batches and quantities in it.

**event bus** — The in-process publisher that carries StockMoved and ReservationLapsed events between modules. Subscribers run synchronously.

**item code** — The code that identifies a SKU. Same as SKU.

**movement** — A transfer of units of a SKU from one bin to another bin. Every change to on-hand is a movement.

**on-hand** — The units of a SKU physically in a bin, counted per bin. Quarantined units are on-hand.

**ORM session** — The SQLAlchemy session. Obtain it through the unit of work, never directly.

**pick list** — The pick tasks handed to one picker for one wave in one zone.

**pick queue** — The released pick tasks waiting to be handed to pickers.

**PickListBuilder** — The class that builds pick lists from the pick queue, one per picker per zone.

**putaway** — Moving received units into bins.

**quantity** — A number of units.

**quarantine** — A bin state. Units in a quarantine bin are on-hand but cannot be reserved, allocated or picked until someone has inspected them.

**receipt** — Goods arriving into the warehouse, recorded at goods-in before putaway.

**reconciliation sweep** — The check that runs inside every movement's unit of work, re-summing the source bin's on-hand from the ledger and rejecting the movement if on-hand would go below zero. Introduced by ADR-0003.

**reservation** — A quantity of a SKU set aside for an order line, not tied to any bin. Distinct from an *allocation*, which names the bins. A reservation lapses after the *reservation TTL*.

**reservation TTL** — How long a reservation holds before it lapses and its quantity is available again. Operators set it per warehouse as `reservation_ttl` in `stockroom.toml`.

**ReservationService** — The service class that creates and lapses reservations, and backorders a line when too little is available.

**return** — Goods a customer sends back against an order. Returned units go into a quarantine bin until inspected.

**shelf** — A shelf in the racking. Operators sometimes say shelf when they mean a bin.

**SKU** — Stock-keeping unit: one sellable product variant, such as one size and colour of a product, tracked as its own line of stock.

**SkuCache** — In-memory cache of SKU records, refreshed every five minutes.

**stock** — The goods held in the warehouse. The stock level of a SKU is its on-hand.

**StockLot** — Named so because "batch" means a batch job here. A StockLot is the units of one SKU received together, sharing an expiry date and a lot number.

**stocktake** — A count of every bin in the warehouse, done with all picking stopped. Distinct from a *cycle count*.

**two-phase pick** — The picking approach adopted in ADR-0004.

**unit of work** — The `uow()` context manager every stock change runs inside. It commits on success and rolls back on error.

**zone** — An area of the warehouse with its own pickers. Pick lists are made per zone.
