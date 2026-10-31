---
# Superseding ADR-0003 is a provisional item marked forced: both in one P item, before the appendix heading.
type: regex
target: { source: file, path: batch.md }
pattern: '(?:^|\n)[#*\s-]*P\d\b(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?(?:ADR-?0003(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?\bforced\b|\bforced\b(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?ADR-?0003)'
flags: i
---
