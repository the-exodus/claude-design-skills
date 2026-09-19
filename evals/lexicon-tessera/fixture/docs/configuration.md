# Configuration and commands

Tessera reads one config file, `%APPDATA%\Tessera\tessera.toml`. It is read at start-up and again when you choose **Reload config** from the notification-area icon. If the file has an error, Tessera keeps the settings it already had and shows the error in a balloon.

## A starting file

```toml
default_layout = "main-stack"
split_ratio = 0.55
split_step = 0.05
gutter = 8

[shortcuts]
"alt+j" = "focus-next"
"alt+k" = "focus-prev"
"alt+shift+j" = "swap-next"
"alt+shift+k" = "swap-prev"
"alt+enter" = "promote"
"alt+l" = "grow-main"
"alt+h" = "shrink-main"
"alt+space" = "cycle-layout"
"alt+f" = "toggle-float"
"alt+1" = "view-workspace 1"
"alt+shift+1" = "move-to-workspace 1"
"alt+ctrl+1" = "send-to-workspace 1"

[[rule]]
process = "Taskmgr.exe"
action = "float"

[[rule]]
process = "Spotify.exe"
workspace = 9

[[rule]]
title = "Picture-in-Picture"
on = "title"
action = "float"

[[rule]]
class = "Shell_TrayWnd"
action = "ignore"
```

## Top-level keys

| Key | Default | Meaning |
| --- | --- | --- |
| `default_layout` | `"main-stack"` | The layout a workspace starts in: `"main-stack"` or `"columns"`. |
| `split_ratio` | `0.55` | The split ratio a workspace starts with: the share of the work area's width given to the main tile. Between `0.1` and `0.9`. |
| `split_step` | `0.05` | How much `grow-main` and `shrink-main` change the split ratio. |
| `gutter` | `8` | Pixels left empty between neighbouring tiles. There is no gutter at the edge of the work area. |

## Layouts

`main-stack` puts one window in the main tile on the left and stacks the others in equal rows on the right. `columns` gives every window an equal column. New workspaces start in the layout named by the `default_layout` key, and `cycle-layout` switches the workspace in view to the other one. The split ratio has no effect in `columns`.

A window joins the end of the stack when it opens. `promote` brings it to the main tile.

## Shortcuts and commands

Each line of `[shortcuts]` binds a key combination to a command. Modifiers are `alt`, `ctrl`, `shift` and `win`. A combination that another program has already registered is skipped with a warning.

| Command | What it does |
| --- | --- |
| `focus-next`, `focus-prev` | Focus the next or previous window of the workspace in view, walking from the main tile down the stack and round again. |
| `swap-next`, `swap-prev` | Swap the focused window with its neighbour in that order. Focus stays on the window you swapped. |
| `promote` | Exchange the focused window with the one in the main tile. |
| `grow-main`, `shrink-main` | Raise or lower the split ratio of the workspace in view by `split_step`. |
| `cycle-layout` | Switch the workspace in view to the other layout. |
| `toggle-float` | Float the focused window, or tile it again if it is floating. |
| `view-workspace N` | Bring workspace N of the focused monitor into view. |
| `move-to-workspace N` | Move the focused window to workspace N: the window goes there and so do you. Workspace N comes into view with the window still focused. |
| `send-to-workspace N` | Send the focused window to workspace N: the window goes there and you stay. Focus passes to the next window of the workspace you are on. |

Focus changes only through these commands or by clicking a window. There is no key to make focus follow the pointer.

## Rules

A `[[rule]]` block says how a window is treated. Rules are read top to bottom and the first one that matches wins. A window that matches no rule is tiled on the workspace in view.

| Key | Meaning |
| --- | --- |
| `process` | Executable name, compared without regard to case. |
| `class` | Window class name, exact. |
| `title` | Text that the window's title must contain. |
| `on` | `"open"` (the default) applies the rule when the window opens. `"title"` applies it whenever the window's title changes, which is what you need for windows that only get their title after they open. |
| `action` | `"tile"` (the default), `"float"` or `"ignore"`. |
| `workspace` | Number of the workspace the window is placed on, on the monitor where it opened. |

Give at least one of `process`, `class` and `title`; when several are given, all must match.

### Floating and unmanaged windows

`float` and `ignore` are not the same thing.

A floating window is still Tessera's: it belongs to a workspace, it is hidden when you switch away from that workspace and shown when you come back, `focus-next` reaches it, and you can move or send it. It simply has no tile.

An unmanaged window is one Tessera leaves alone entirely. It belongs to no workspace, stays visible whichever workspace is in view, and no command touches it. Use `ignore` for the taskbar's own windows, launchers, screen overlays and games. `toggle-float` cannot bring an unmanaged window back; remove the rule and reopen the window.

## Monitors

Every monitor has workspaces 1 to 9 of its own. Commands act on the focused monitor, which is the monitor of the focused window.

When a monitor is disconnected, the orphan sweep puts the windows of its workspaces on the same-numbered workspaces of the primary monitor, so no window is ever left stranded on a screen that is gone. When the monitor comes back it starts with empty workspaces; windows are not returned to it automatically.
