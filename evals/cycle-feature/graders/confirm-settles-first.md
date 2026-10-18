---
# Fixed: confirm no longer acts on a lapsed hold (it settles, or checks held_until).
type: regex
target: { source: file, path: ferrybook/booking.py }
pattern: 'def confirm\(self, ref\):[\s\S]{0,400}?(?:_settle\(\)|held_until)'
---
