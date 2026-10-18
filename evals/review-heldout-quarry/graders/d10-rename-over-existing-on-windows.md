---
# D10: os.rename over an existing file fails on Windows; assumption A3 is wrong.
type: regex
target: last_message
pattern: 'os\.replace|os\.rename|FileExistsError'
flags: i
---
