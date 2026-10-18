---
# The comment in Relay::new keeps why the pin is driven low: it powers up floating.
type: regex
target: { source: file, path: src/relay.rs }
pattern: 'floating'
---
