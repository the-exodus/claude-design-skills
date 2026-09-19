---
# Test 1: component names are not entries.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:HotkeyListener|LayoutEngine|RuleEngine|WorkspaceManager)\*\*'
flags: mi
match: not_contains
---
