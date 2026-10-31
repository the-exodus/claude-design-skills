---
# The reply opens with the objection: ADR-0004 named as unprotected within its first 900 characters.
type: regex
target: last_message
pattern: '^(?=[\s\S]{0,900}?ADR-?0004)(?=[\s\S]{0,900}?(?:unprotected|not protected|isn.t protected|not enforced|unenforced|isn.t enforced|no test|nothing fail|still pass|passe[sd]|stop))'
flags: i
---
