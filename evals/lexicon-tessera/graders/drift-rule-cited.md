---
# Drift at a known line: enum RuleTrigger at src/Tessera/Rules/Rule.cs:4-11, or its use at RuleEngine.cs:33-37.
type: regex
target: last_message
pattern: 'Rule\.cs[^\n\w]{0,4}(?:lines?\s*|L)?(?:[3-9]|1[01])\b|RuleEngine\.cs[^\n\w]{0,4}(?:lines?\s*|L)?(?:3[3-7])\b'
---
