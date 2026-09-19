---
# All five inherited entries stand word for word: none of them changed meaning in this interview.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^(?=[\s\S]*\*\*cycle\*\* — One run of gaugefeed over every station in the \*station list\*\. Cycles are five minutes apart\.)(?=[\s\S]*\*\*reading\*\* — One water level reported by a \*station\*, with the time gaugefeed fetched it\. Not the time of measurement, which the stations do not report\.)(?=[\s\S]*\*\*stale\*\* — Said of a \*reading\* older than two \*cycles\*\. A stale reading is still shown; it is not the same as having no reading\.)(?=[\s\S]*\*\*station\*\* — A river gauge that answers requests for its current \*reading\*, identified by its URL\.)(?=[\s\S]*\*\*station list\*\* — The \*stations\* gaugefeed asks each \*cycle\*, one URL per line\.)'
---
