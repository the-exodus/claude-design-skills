# Agent notes

Cinder is the controller for the studio's electric kiln: a Raspberry Pi reads a
MAX31855 thermocouple amplifier over SPI and switches the elements through a
solid-state relay. `cargo test` runs everything; the hardware is faked in tests.

## Comments

- Decisions are recorded in `docs/decisions/`, numbered. Code in `src/` may cite
  one by its number, for example "(0003)".
- Comments in `tests/` don't cite documents or decision records. A test comment
  whose only content is a pointer to a document is removed, not re-sourced.
- `tests/architecture/` checks the structural rules, and its comments may cite
  the record a rule comes from, but only beside their own statement of what the
  test checks. A citation never stands in for the claim.

Domain words are defined in `docs/glossary.md`; use them as written there.
