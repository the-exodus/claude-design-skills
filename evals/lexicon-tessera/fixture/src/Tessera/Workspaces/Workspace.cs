using System;
using System.Collections.Generic;
using System.Linq;
using Tessera.Layouts;

namespace Tessera.Workspaces;

/// <summary>How a managed window takes part in its workspace.</summary>
public enum WindowMode
{
    /// <summary>The window has a tile.</summary>
    Tiled,

    /// <summary>The window floats above the tiles at bounds of its own.</summary>
    Floating,
}

/// <summary>A window Tessera manages. Unmanaged windows never get one of these.</summary>
public sealed class ManagedWindow
{
    public ManagedWindow(IntPtr handle, string process, string @class, string title)
    {
        Handle = handle;
        Process = process;
        Class = @class;
        Title = title;
    }

    public IntPtr Handle { get; }
    public string Process { get; }
    public string Class { get; }
    public string Title { get; set; }
    public WindowMode Mode { get; set; } = WindowMode.Tiled;

    /// <summary>Where the window sits while it floats. Meaningless while it is tiled.</summary>
    public Rect FloatBounds { get; set; }
}

/// <summary>
/// One numbered workspace of one monitor: its windows in order, its layout and its
/// split ratio. The first tiled window is the one in the main tile.
/// </summary>
public sealed class Workspace
{
    private readonly List<ManagedWindow> _windows = new();

    public Workspace(int number, MonitorInfo monitor, ILayout layout, double splitRatio)
    {
        Number = number;
        Monitor = monitor;
        Layout = layout;
        SplitRatio = splitRatio;
    }

    public int Number { get; }
    public MonitorInfo Monitor { get; internal set; }
    public ILayout Layout { get; set; }
    public double SplitRatio { get; set; }

    /// <summary>True for the one workspace of its monitor whose windows are shown.</summary>
    public bool InView { get; internal set; }

    /// <summary>Every window of the workspace, tiled and floating, in order.</summary>
    public IReadOnlyList<ManagedWindow> Windows => _windows;

    /// <summary>The tiled windows, in the order the layout receives them.</summary>
    public IEnumerable<ManagedWindow> Tiled => _windows.Where(w => w.Mode == WindowMode.Tiled);

    /// <summary>
    /// Number of tiled windows. Callers that draw borders care about the single-window
    /// case, which the layouts treat specially.
    /// </summary>
    public int TiledCount => Tiled.Count();

    /// <summary>Adds a window at the end of the order, which for a tiled window is the end of the stack.</summary>
    public void Add(ManagedWindow window) => _windows.Add(window);

    public bool Remove(ManagedWindow window) => _windows.Remove(window);

    /// <summary>
    /// The window after (step 1) or before (step -1) the given one, wrapping round.
    /// Returns null when the workspace has no other window.
    /// </summary>
    public ManagedWindow? Neighbour(ManagedWindow window, int step)
    {
        if (_windows.Count < 2)
            return null;
        int i = _windows.IndexOf(window);
        return _windows[(i + step + _windows.Count) % _windows.Count];
    }

    /// <summary>Gives the focus to a window of this workspace and records it as focused.</summary>
    public void Focus(WmContext ctx, ManagedWindow window)
    {
        ctx.Focused = window;
        ctx.Mover.Focus(window.Handle);
    }

    /// <summary>Exchanges the places of two windows in the order.</summary>
    public void Swap(ManagedWindow a, ManagedWindow b)
    {
        int i = _windows.IndexOf(a), j = _windows.IndexOf(b);
        (_windows[i], _windows[j]) = (_windows[j], _windows[i]);
    }

    /// <summary>
    /// Promotes a window: exchanges it with the window in the main tile. Promoting the
    /// window that is already there, or a floating window, does nothing.
    /// </summary>
    public void Promote(ManagedWindow window)
    {
        var main = Tiled.FirstOrDefault();
        if (main is null || main == window || window.Mode != WindowMode.Tiled)
            return;
        Swap(main, window);
    }
}
