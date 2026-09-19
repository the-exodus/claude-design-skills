---
# No component or identifier anywhere in the written lexicon. Case-sensitive.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '\b(?:HotkeyListener|LayoutEngine|RuleEngine|WorkspaceManager|WindowMover|WmContext|SecondaryArea|RuleTrigger|RuleAction)\b|\bctx\b'
match: not_contains
---
