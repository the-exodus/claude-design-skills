---
# The doc on Relay::set, a restatement of its signature, is gone.
type: regex
target: { source: file, path: src/relay.rs }
pattern: 'Sets[\s/]+the[\s/]+relay[\s/]+on[\s/]+or[\s/]+off'
flags: i
match: not_contains
---
