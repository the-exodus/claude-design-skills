# 0003. Rules may be re-applied when a window's title changes

## Status

Accepted, November 2023.

## Context

Rules were first applied exactly once, at the moment a window opened. That fails for windows that do not yet have their final title at that moment. A browser's picture-in-picture window opens with an empty title and is named a moment later; several Electron applications open a splash window that turns into the main window by changing its title. A `title` match in a rule could never catch these, and people ended up floating them by hand every time.

## Decision

A rule carries a trigger. `on = "open"`, the default, applies the rule when the window opens, as before. `on = "title"` applies the rule whenever the title of a managed window changes. Both kinds live in the same list and the first match for the trigger at hand wins.

## Consequences

- A window can change from tiled to floating, or the other way, in the middle of its life, and the workspace is rearranged when it does.
- A `title` rule with `action = "ignore"` releases a window that was managed until then.
- The reverse is not possible: unmanaged windows are not watched, so no rule can bring one back under management.
- Title changes are frequent (browsers retitle on every tab switch), so matching on this trigger has to stay cheap: plain string comparison, no regular expressions.
