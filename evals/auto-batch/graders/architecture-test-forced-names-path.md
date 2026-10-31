---
# Changing the architecture test is a provisional item marked forced that names the protected path, both in one P item.
type: regex
target: { source: file, path: batch.md }
pattern: '(?:^|\n)[#*\s-]*P\d\b(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?(?:tests/test_architecture\.py(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?\bforced\b|\bforced\b(?:(?!\n[#*\s-]*P\d\b)(?!\n(?:#{1,6}|\*\*)[^\n]{0,12}appendix|\nappendix\s*\n)[\s\S])*?tests/test_architecture\.py)'
flags: i
---
