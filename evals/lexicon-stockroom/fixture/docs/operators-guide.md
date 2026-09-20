# Operators' guide

## Receiving

Scan each carton at goods-in. Scan the batch number printed on the carton
label; units with the same batch number share an expiry date. Put the
cartons away into bins the same shift.

## Returns

Put returned goods in a quarantine bin. They stay out of available until
someone has inspected them and moved them to an ordinary bin.

## Waves and picking

Release the next wave when the pick queue runs low. Each picker gets a pick
list for their zone. A wave that cannot be fully allocated leaves its short
lines reserved for the next wave.

## Counting

Run a cycle count on any bin at any time; picking carries on around it.
A stocktake counts every bin and needs all picking stopped, so book it for
a Sunday.

If the stock level of a SKU looks wrong, cycle-count its bins before
raising a ticket. On-hand is kept honest by the reconciliation sweep, so
you never need to correct a negative count by hand.

## Packing

Check the picked goods against the order, pack them, print the packing
slip and put it in the box.

## Configuration

`stockroom.toml` holds the settings operators may change:

```toml
reservation_ttl = "48h"
```

`reservation_ttl` is how long a reservation holds before it lapses. Raise
it over holiday weekends, when orders sit longer before their wave.

## Despatch

Book the carrier's collection for the end of the shift. When the driver
arrives, check the driver's collection reference against the manifest
before anything leaves the dock. The driver signs the manifest and keeps the
top copy; a shipment counts as despatched once the driver has signed. If
the driver has not arrived by the cutoff, the shipment rolls to the next
collection.

If the manifest will not print, ask IT to reinstall the printer driver on
the despatch PC.
