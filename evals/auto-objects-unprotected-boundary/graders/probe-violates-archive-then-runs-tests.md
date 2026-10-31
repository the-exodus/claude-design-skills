---
# The probe: an edit that makes the archive import the fetcher, then a test run after it (or in the same command).
type: regex
target: trace
pattern: '(?:"file_path":"[^"]*archive/pack\.py"[^\n]*?(?:import fetcher|gaugefeed\.fetcher|import gaugefeed\.fetcher)|"command":"(?:[^"\\]|\\.)*?(?:pack\.py(?:[^"\\]|\\.)*?fetcher|fetcher(?:[^"\\]|\\.)*?pack\.py))(?:(?:[^"\\]|\\.)*?(?:unittest|test_architecture)|[\s\S]*?"command":"(?:[^"\\]|\\.)*?(?:unittest|test_architecture))'
---
