# HTTP API

## GET /skus/{code}

Returns the SKU with its `available` field: on-hand less open reservations,
with quarantine bins left out.

## POST /orders/{order}/lines/{line}/reserve

Reserves the line's quantity. If too little is available the line is
backordered instead and waits for the next receipt.

## POST /waves/{wave}/release

Releases a wave: its reserved lines are allocated and their pick tasks
enter the pick queue.

## POST /bins/{bin}/counts

Body: `{"sku": "...", "counted": 12}`. Posts a cycle count for one SKU in
one bin; the difference from on-hand is posted as an adjustment.
