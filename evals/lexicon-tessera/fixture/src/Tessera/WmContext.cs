using System;
using System.Collections.Generic;
using Tessera.Config;
using Tessera.Layouts;
using Tessera.Rules;
using Tessera.Workspaces;

namespace Tessera;

/// <summary>
/// A monitor as Windows reports it: its handle, its device name and its work area,
/// which is the screen minus the taskbar and any docked toolbars.
/// </summary>
public sealed record MonitorInfo(IntPtr Handle, string DeviceName, Rect WorkArea, bool IsPrimary);

/// <summary>
/// Moves, shows, hides and focuses native windows. Implemented in Tessera.Native by
/// <c>WindowMover</c>, which batches placements through DeferWindowPos.
/// </summary>
public interface IWindowMover
{
    /// <summary>Applies every placement in one batch, in the order given (last is topmost).</summary>
    void Apply(IReadOnlyList<(IntPtr Handle, Rect Bounds)> placements);

    /// <summary>Shows a window that <see cref="Hide"/> hid.</summary>
    void Show(IntPtr handle);

    /// <summary>Hides a window without minimizing or closing it.</summary>
    void Hide(IntPtr handle);

    /// <summary>Gives a window the keyboard focus and brings it to the foreground.</summary>
    void Focus(IntPtr handle);

    /// <summary>Reads a window's current bounds, used when a window starts to float.</summary>
    Rect BoundsOf(IntPtr handle);
}

/// <summary>
/// The context (lexicon: context) handed to every command and service method as its
/// first argument: the settings, the monitors, the services and the focused window.
/// There is exactly one, created at start-up and alive until Tessera quits.
/// </summary>
public sealed class WmContext
{
    public WmContext(TesseraConfig config, IWindowMover mover, IReadOnlyList<MonitorInfo> monitors)
    {
        Config = config;
        Mover = mover;
        Monitors = new List<MonitorInfo>(monitors);
        Layouts = new LayoutEngine();
        Rules = new RuleEngine();
        Workspaces = new WorkspaceManager(this);
    }

    /// <summary>The settings currently in force. Replaced wholesale on reload.</summary>
    public TesseraConfig Config { get; set; }

    /// <summary>The platform service that moves windows.</summary>
    public IWindowMover Mover { get; }

    /// <summary>The monitors currently connected, primary first.</summary>
    public List<MonitorInfo> Monitors { get; }

    public LayoutEngine Layouts { get; }

    public RuleEngine Rules { get; }

    public WorkspaceManager Workspaces { get; }

    /// <summary>The window that has the focus, or null when no managed window has it.</summary>
    public ManagedWindow? Focused { get; set; }

    /// <summary>
    /// Handles of windows Tessera leaves alone because a rule said to ignore them.
    /// They belong to no workspace and no command touches them.
    /// </summary>
    public HashSet<IntPtr> Unmanaged { get; } = new();

    /// <summary>The monitor of the focused window, or the primary monitor when nothing is focused.</summary>
    public MonitorInfo FocusedMonitor =>
        Focused is { } w ? Workspaces.WorkspaceOf(w).Monitor : Monitors[0];

    /// <summary>Writes a line to the log file beside the config file.</summary>
    public void Log(string message) =>
        System.Diagnostics.Trace.WriteLine($"{DateTime.Now:HH:mm:ss} {message}");
}
