# Working on Lockerline

Build with `./gradlew build`; the tests run on the fake lock board, so no hardware is needed.

Words come from `docs/lexicon.md`. Decisions are in `docs/adr/`.

## Comments and records

- In `src/`, a comment may cite an ADR by number (`ADR-0004`).
- In `tests/`, comments describe the code under test and the harness, never the documents: no ADR or document is cited, and a comment that only points at one is removed rather than re-pointed.
- `tests/architecture/` is the exception. Those tests guard decisions, so a comment there may cite the ADR it protects, beside its own words saying what is checked.
