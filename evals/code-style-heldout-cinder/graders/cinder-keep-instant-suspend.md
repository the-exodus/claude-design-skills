---
# The comment on SystemClock::now keeps that Instant stops during suspend on Linux.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'suspend'
---
