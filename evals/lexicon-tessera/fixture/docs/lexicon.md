# Tessera lexicon

Started in March 2023 alongside the first layout work; entries are added in the pull request that introduces a new class, command or config key.

Gaps: none.

A term earns an entry when the team has given something a name, whether in code, in a decision record or in conversation, so that every name has one place where it is explained.

---

**click-to-focus policy** — Focus changes only when the user runs a focus command or clicks a window; moving the mouse pointer over a window never focuses it. Chosen so that a stray movement of the pointer cannot redirect what the user is typing.

**config file** — The text file in which the user writes their settings.

**context** — The object that carries the monitors, the loaded settings and the focused window, and that every command, handler and service receives as its first argument. Written `ctx` in code.

**floating window** — A window that belongs to a *workspace* but has no *tile*: it keeps the size and position the user gives it, is drawn above the tiled windows, and is hidden and shown with its *workspace*. The `WorkspaceManager` tracks it like any other window.

**HotkeyListener** — The service that registers the user's *shortcuts* with Windows and turns each key press into a command.

**layout** — The scheme by which a *workspace*'s tiled windows get their *tiles*: main-stack or columns. A *workspace* has one layout at a time, which the user can cycle. Main-stack puts one window in the *main tile* on the left and stacks the others in equal rows on the right; columns gives every window an equal column. New workspaces start in the layout named by the `default_layout` key. The `LayoutEngine` asks the layout for rectangles and hands them to the `WindowMover`, which repositions all the windows in a single batch. When a *workspace* holds a single window, every layout gives it the whole *work area*. Because a layout is a pure function of the window count, the *work area*, the *split ratio* and the gutter, it cannot remember sizes, so dragging the edge of a tiled window has no lasting effect. The default was columns until 0.4; it became main-stack because on ultrawide monitors equal columns pushed the editor off-centre.

**LayoutEngine** — The class that asks a *workspace*'s *layout* for rectangles and applies them to the windows.

**main tile** — The *tile* on the left of the *work area* in the main-stack *layout*, meant for the window the user is working in. Its width is set by the *split ratio*; the other windows share the stack to its right.

**move** — To relocate the focused window to another *workspace* and take the user there with it: the target *workspace* comes into view and the window stays focused.

**orphan sweep** — The routine that runs when a monitor is disconnected and re-homes the windows of that monitor's *workspaces* onto the primary monitor, so that no window is left on a screen that no longer exists.

**pane** — The rectangle of a monitor's *work area* occupied by one tiled window.

**rule** — A user-written instruction that matches windows by process name, window class or title and says how to treat them: tile, float, ignore, or place on a given *workspace*. A rule is applied only once, when the window first opens; nothing that happens to the window afterwards ever triggers a rule again.

**RuleEngine** — The component that matches windows against the user's *rules* and returns the action to take.

**send** — To relocate the focused window to another *workspace* while the user stays where they are: the window leaves the view and focus passes to the next window. Not to be confused with *move*, which takes the user along.

**shortcut** — A key combination the user presses to run a command.

**split ratio** — The share of the *work area*'s width given to the *main tile*. Users set a starting value and nudge it per *workspace* with the grow and shrink commands.

**tile** — The rectangle of a monitor's *work area* that a *layout* assigns to one window. Tiles never overlap, and together they cover the *work area* apart from the gutters between them.

**unmanaged window** — See *floating window*.

**work area** — The part of a monitor that windows may occupy: the whole screen minus the taskbar and any docked toolbars. *Tiles* are cut from the work area, never from the full screen.

**workspace** — A numbered set of windows belonging to one monitor. Exactly one workspace per monitor is in view at a time; the windows of the others are hidden. Each workspace has its own *layout* and *split ratio*.

**WorkspaceManager** — The class that owns every *workspace*, decides which is in view on each monitor, and carries out *move* and *send*.

**zoom** — To exchange the focused window with the window in the *main tile*, so that the focused window becomes the main one.
