---
# No type, routine or identifier anywhere in the written glossary. Case-sensitive.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '\b(?:HerdStore|ListBuilder|MeterIngest|GroupManager|LactationService|TreatmentService|Insemination|Env)\b|sweepWithheld'
match: not_contains
---
