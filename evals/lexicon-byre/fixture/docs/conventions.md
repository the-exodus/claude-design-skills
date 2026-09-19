# Code conventions

Short, and mostly about names.

## Names

- Identifiers take their words from the [glossary](glossary.md). If the
  glossary says "dry off", the code says `DryOff`, not `EndLactation` or
  `StopMilking`.
- Every new exported type gets a glossary entry in the same pull request, so
  that the glossary and the code never fall out of step.
- A service, in the breeding sense, is `Insemination` in code and never
  `Service`: here `Service` already means a long-lived component such as
  `TreatmentService`, and the two senses in one package were unreadable.
- Ear tags are `Tag string` everywhere. Never parse them; farms reuse and
  reformat them.

## Shape

- `env.Env` is the first argument of every operation that reads a setting,
  the time or the database. Nothing calls `time.Now` directly.
- Long-lived components are named `...Service`, `...Manager`, `...Store` or
  `...Builder` and are built once in `cmd/byre`.
- Record types (`Animal`, `Milking`, `Lactation`, `Treatment`) carry data and
  small questions about that data (`IsHeifer`, `DaysInMilk`). They do not
  reach the database.

## Comments and errors

- A doc comment starts with the name it documents and says what the thing
  does for the herd manager before it says how.
- Wrap errors with `%w` and name the ear tag in the message when there is one.
- Dates are farm-local calendar days. Use `Env.Today`, not truncation.
- Yield is kilograms, as the meters report it. Convert to litres only when
  printing, and only if the farm asks.
