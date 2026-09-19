# 0002. Focus does not follow the pointer

## Status

Accepted, June 2023.

## Context

Several tiling window managers on other platforms focus whichever window the pointer is over. We were asked for the same. On Windows it needs a low-level mouse hook, which antivirus products dislike and which adds latency to every pointer movement system-wide. It also fights the keyboard-first way Tessera is meant to be used: a nudge of the mouse while typing sends the rest of the sentence to another window.

## Decision

Focus changes only when the user runs a focus command or clicks a window. Tessera installs no mouse hook, and there is no setting to turn pointer-driven focus on.

## Consequences

- Typing is never redirected by a stray movement of the pointer.
- Tessera needs no hook beyond the window-event hook it already has, so it keeps working alongside security software that blocks input hooks.
- People who are used to pointer-driven focus elsewhere will ask for it again. The answer is this record.
- After `send-to-workspace` or a window closing, Tessera has to choose the next focused window itself; it takes the next window in the workspace's order.
