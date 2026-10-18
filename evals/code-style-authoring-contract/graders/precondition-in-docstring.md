---
# The caller's precondition, that a write waits on or fails during a roast because Artisan holds the lock from charge to drop, is in a docstring in log.py: on save, or on the class. Matched on its meaning.
type: regex
target: { source: file, path: roastlog/log.py }
pattern: '"""(?:(?!""")[\s\S])*?(lock|busy|during a roast|roast is in progress|in progress|charge(d)? (and|to|until) (the )?drop|between roasts|Artisan)(?:(?!""")[\s\S])*?"""'
flags: i
---
