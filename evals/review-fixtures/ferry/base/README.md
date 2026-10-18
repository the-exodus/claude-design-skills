# Ferrybook

Ferrybook takes bookings for the operator's sailings and prices them.

## Bookings

A booking is for one passenger on one sailing, with or without a car. A booking is confirmed when it is made, and its reference is printed on the ticket. Cancelling a booking frees its space at once.

A sailing keeps `reserved_car_spaces` car spaces back for emergency vehicles; they are never sold.

## Fares

Fares are in øre. A car costs the route's car fare, a foot passenger the foot fare. When fewer than `surge_threshold` car spaces are left, car fares rise by `surge_percent`. Children travel at half the foot fare.

## Configuration

`defaults.json` holds the shipped settings:

| Key | Default | Meaning |
|---|---|---|
| `reserved_car_spaces` | `2` | Car spaces per sailing kept for emergency vehicles |
| `surge_threshold` | `5` | Car spaces left below which surge pricing applies |
| `surge_percent` | `20` | Surge added to the car fare, in percent |
