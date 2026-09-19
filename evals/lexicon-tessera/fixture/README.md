# Tessera

Tessera is a tiling window manager for Windows. Instead of leaving windows wherever they happen to open, it arranges the windows on each monitor into tiles that never overlap, and it lets you drive all of it from the keyboard.

## What it does

- **Tiles your windows.** Every monitor's work area is divided among the windows on it. In the default main-stack layout one window takes the main tile on the left and the others share the stack on the right. Open a window and it joins the stack; close one and the stack closes up.
- **Workspaces per monitor.** Each monitor has nine numbered workspaces, one of which is in view. Switch workspace and the windows of the old one are hidden, not closed.
- **Keyboard first.** Walk focus through the stack, swap windows, promote the focused window to the main tile, change the split ratio, and move or send windows to other workspaces, all with shortcuts you choose. Focus never jumps because the pointer wandered over another window.
- **Floating windows.** Some windows do not tile well: dialogs, calculators, video players. Float them and they sit above the tiles at whatever size you like, while still belonging to their workspace.
- **Rules.** Write rules in the config file to say how new windows are treated: tile them, float them, put them on a given workspace, or have Tessera ignore them so they stay unmanaged.
- **No stranded windows.** Tessera never strands a window on a screen that is gone. Unplug a monitor and the windows of its workspaces go to the same-numbered workspaces of the primary monitor.

## Getting started

1. Install the .NET 8 desktop runtime.
2. Put `tessera.toml` in `%APPDATA%\Tessera\`. A starting file is in [docs/configuration.md](docs/configuration.md).
3. Run `Tessera.exe`. It lives in the notification area; right-click the icon to reload the config file or quit.

Windows that were already open are tiled when Tessera starts. Quit Tessera and every hidden window is shown again where it was.

## Documentation

- [Configuration and commands](docs/configuration.md): every key of the config file, every command you can bind to a shortcut, and how rules work.
- [Lexicon](docs/lexicon.md): the words we use when talking about Tessera.
- [Decision records](docs/adr/README.md): why some things are the way they are.
- [Code conventions](docs/conventions.md): for contributors.

## Building

```
dotnet build src/Tessera
```

The Win32 interop layer (`Tessera.Native`) is a separate project and is not needed to read or change the code under `src/Tessera`.

## Status

Tessera is used daily by its authors and a handful of others. It handles ordinary desktop applications well. Known rough edges: elevated windows cannot be moved unless Tessera itself runs elevated, and some games in borderless mode should be given an `ignore` rule.
