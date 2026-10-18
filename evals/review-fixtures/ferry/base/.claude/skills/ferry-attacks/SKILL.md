---
name: ferry-attacks
description: Ferrybook's own attack list for the adversarial review lens. Not for ordinary sessions.
disable-model-invocation: true
metadata:
  review-lens:
    applies-to: ["ferrybook/**"]
    extends: adversarial
---

# Ferry attacks

Attacks that have broken Ferrybook before, in addition to the generic ones:

- A sailing whose departure passes while bookings or holds on it are still open: what each operation does with a sailing in the past.
- The same passenger on one sailing twice, by two paths (a booking and a waitlist entry, or two bookings made in one operation).
- A cancelled booking's ticket presented again: anything that could issue its reference to someone else.
- The book built from `defaults.json` with `make_book`, not the bare constructor the unit tests use: reserved car spaces and surge settings are on there.

Prove an attack with a throwaway test in `tests/test_attack_<topic>.py` using `tests/helpers.sailing`, and run it with `python3 -m unittest tests.test_attack_<topic>`.
