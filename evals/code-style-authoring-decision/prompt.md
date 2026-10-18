---
description: "Authoring, the ADR seam. A small decision the user keeps out of an ADR: its reason is said beside the code it explains, nothing added only restates, and no record is written."
tags: [code-style, authoring]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add the development ratio to each line of the day report: development time as a share of total roast time, as a whole percent, rounded down. Round down, not to nearest: the roaster's own screen rounds down, and people hold the printed report up against it, so 19.9 has to print as 19. Leave a dash when the roast has no first crack or no drop recorded. This is too small a call for an ADR, so don't write one.
