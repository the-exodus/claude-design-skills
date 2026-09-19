# Contributing

- Name code after the terms in `GLOSSARY.md`.
- When you add a service or engine class, add a glossary entry for it.
- Every stock change goes through `uow()`; never open an ORM session
  directly.
- Every movement goes through `post_movement()`.
- A module docstring may point to the glossary entry for its main class.
- Record decisions in `docs/decisions/` and add them to the index.
