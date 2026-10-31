---
# The record draws a boundary and an architecture test protects it, so its Decision carries design:adr's fixed sentence.
type: regex
target: { source: file, path: docs/adr/0005-the-flood-page-reads-levels-only-through-the-readings-module.md }
pattern: '^## Decision[\s\S]*The architecture tests enforce this boundary\.[\s\S]*^## Consequences'
flags: m
---
