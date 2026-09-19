using System;
using System.Collections.Generic;
using Tessera.Workspaces;

namespace Tessera.Input;

/// <summary>Registers key combinations with Windows. Implemented in Tessera.Native over RegisterHotKey.</summary>
public interface IHotkeyRegistrar
{
    /// <summary>Returns false when another program already holds the combination.</summary>
    bool TryRegister(int id, string combination);

    void UnregisterAll();
}

/// <summary>
/// Registers the user's shortcuts and runs the command bound to each when it is pressed.
/// Focus only ever changes here or through a click; nothing in Tessera watches the pointer.
/// </summary>
public sealed class HotkeyListener
{
    private readonly IHotkeyRegistrar _registrar;
    private readonly Dictionary<int, string> _commands = new();

    public HotkeyListener(IHotkeyRegistrar registrar) => _registrar = registrar;

    /// <summary>Registers every shortcut of the settings in force, dropping any registered before.</summary>
    public void Register(WmContext ctx)
    {
        _registrar.UnregisterAll();
        _commands.Clear();
        int id = 1;
        foreach (var (combination, command) in ctx.Config.Shortcuts)
        {
            if (_registrar.TryRegister(id, combination))
                _commands[id++] = command;
            else
                ctx.Log($"shortcut {combination} is taken by another program; skipped");
        }
    }

    /// <summary>Called from the message loop on WM_HOTKEY.</summary>
    public void OnHotkey(WmContext ctx, int id)
    {
        if (_commands.TryGetValue(id, out var command))
            Run(ctx, command);
    }

    /// <summary>Runs one command, written as in the config file, such as "send-to-workspace 3".</summary>
    public void Run(WmContext ctx, string command)
    {
        var parts = command.Split(' ', 2, StringSplitOptions.TrimEntries);
        var manager = ctx.Workspaces;
        var here = manager.InViewOn(ctx.FocusedMonitor);
        Workspace Numbered() => manager.Get(ctx.FocusedMonitor, int.Parse(parts[1]));

        if (parts[0] == "view-workspace")
        {
            manager.View(ctx, Numbered());
            return;
        }
        if (parts[0] == "cycle-layout")
        {
            here.Layout = ctx.Layouts.Next(here.Layout);
            ctx.Layouts.Arrange(ctx, here);
            return;
        }

        // Every other command acts on the focused window.
        if (ctx.Focused is not { } focused)
            return;

        switch (parts[0])
        {
            case "focus-next" or "focus-prev":
                if (here.Neighbour(focused, parts[0] == "focus-next" ? 1 : -1) is { } target)
                    here.Focus(ctx, target);
                return;
            case "swap-next" or "swap-prev":
                if (here.Neighbour(focused, parts[0] == "swap-next" ? 1 : -1) is { } other)
                    here.Swap(focused, other);
                break;
            case "promote":
                here.Promote(focused);
                break;
            case "grow-main" or "shrink-main":
                double step = parts[0] == "grow-main" ? ctx.Config.SplitStep : -ctx.Config.SplitStep;
                here.SplitRatio = Math.Clamp(here.SplitRatio + step, 0.1, 0.9);
                break;
            case "toggle-float":
                if (focused.Mode == WindowMode.Tiled)
                    focused.FloatBounds = ctx.Mover.BoundsOf(focused.Handle);
                focused.Mode = focused.Mode == WindowMode.Tiled ? WindowMode.Floating : WindowMode.Tiled;
                break;
            case "move-to-workspace":
                manager.MoveTo(ctx, focused, Numbered());
                return;
            case "send-to-workspace":
                manager.SendTo(ctx, focused, Numbered());
                return;
            default:
                ctx.Log($"unknown command \"{command}\"");
                return;
        }
        ctx.Layouts.Arrange(ctx, here);
    }
}
