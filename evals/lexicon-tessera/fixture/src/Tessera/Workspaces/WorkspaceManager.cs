using System;
using System.Collections.Generic;
using System.Linq;
using Tessera.Rules;

namespace Tessera.Workspaces;

/// <summary>Owns every workspace of every monitor, decides which is in view, and carries windows between them.</summary>
public sealed class WorkspaceManager
{
    public const int PerMonitor = 9;
    private readonly List<Workspace> _all = new();

    public WorkspaceManager(WmContext ctx)
    {
        foreach (var monitor in ctx.Monitors)
            AddMonitor(ctx, monitor);
    }

    /// <summary>Gives a newly connected monitor its workspaces, with workspace 1 in view.</summary>
    public void AddMonitor(WmContext ctx, MonitorInfo monitor)
    {
        var layout = ctx.Layouts.Get(ctx.Config.DefaultLayout);
        for (int n = 1; n <= PerMonitor; n++)
            _all.Add(new Workspace(n, monitor, layout, ctx.Config.SplitRatio) { InView = n == 1 });
    }

    public Workspace Get(MonitorInfo monitor, int number) =>
        _all.First(w => w.Monitor.Handle == monitor.Handle && w.Number == number);
    public Workspace InViewOn(MonitorInfo monitor) =>
        _all.First(w => w.Monitor.Handle == monitor.Handle && w.InView);
    public Workspace WorkspaceOf(ManagedWindow window) => _all.First(w => w.Windows.Contains(window));

    /// <summary>
    /// Takes in a window that has just opened, applying the first matching rule with the Open
    /// trigger. A window the rule says to ignore is recorded as unmanaged and null is returned.
    /// </summary>
    public ManagedWindow? Adopt(WmContext ctx, IntPtr handle, WindowFacts facts, MonitorInfo openedOn)
    {
        var rule = ctx.Rules.FirstMatch(ctx, facts, RuleTrigger.Open);
        if (rule?.Action == RuleAction.Ignore)
        {
            ctx.Unmanaged.Add(handle);
            return null;
        }

        var window = new ManagedWindow(handle, facts.Process, facts.Class, facts.Title);
        if (rule?.Action == RuleAction.Float)
            (window.Mode, window.FloatBounds) = (WindowMode.Floating, ctx.Mover.BoundsOf(handle));
        var target = rule?.Workspace is int n ? Get(openedOn, n) : InViewOn(openedOn);
        target.Add(window);
        if (!target.InView) ctx.Mover.Hide(handle);
        ctx.Layouts.Arrange(ctx, target);
        return window;
    }

    /// <summary>Brings a workspace into view on its monitor and hides the one that was.</summary>
    public void View(WmContext ctx, Workspace target)
    {
        var current = InViewOn(target.Monitor);
        if (current == target) return;
        foreach (var w in current.Windows) ctx.Mover.Hide(w.Handle);
        current.InView = false;
        target.InView = true;
        foreach (var w in target.Windows) ctx.Mover.Show(w.Handle);
        ctx.Layouts.Arrange(ctx, target);
    }

    /// <summary>Moves a window: it goes to the target workspace, which comes into view with the window still focused.</summary>
    public void MoveTo(WmContext ctx, ManagedWindow window, Workspace target)
    {
        var source = WorkspaceOf(window);
        if (source == target) return;
        source.Remove(window);
        target.Add(window);
        View(ctx, target);
        ctx.Focused = window;
        ctx.Mover.Focus(window.Handle);
    }

    /// <summary>Sends a window: it goes to the target workspace and the user stays; focus passes to the next window here.</summary>
    public void SendTo(WmContext ctx, ManagedWindow window, Workspace target)
    {
        var source = WorkspaceOf(window);
        if (source == target) return;
        var next = source.Neighbour(window, 1);
        source.Remove(window);
        target.Add(window);
        if (!target.InView) ctx.Mover.Hide(window.Handle);
        ctx.Focused = next;
        if (next is not null) ctx.Mover.Focus(next.Handle);
        ctx.Layouts.Arrange(ctx, source);
        ctx.Layouts.Arrange(ctx, target);
    }

    /// <summary>
    /// The orphan sweep. Runs when a monitor is disconnected: the windows of each of its workspaces
    /// go to the same-numbered workspace of the primary monitor, and the emptied ones are dropped.
    /// </summary>
    public void SweepOrphans(WmContext ctx, MonitorInfo gone)
    {
        ctx.Monitors.RemoveAll(m => m.Handle == gone.Handle);
        foreach (var orphan in _all.Where(w => w.Monitor.Handle == gone.Handle).ToList())
        {
            var home = Get(ctx.Monitors[0], orphan.Number);
            foreach (var w in orphan.Windows.ToList())
            {
                orphan.Remove(w);
                home.Add(w);
                if (home.InView) ctx.Mover.Show(w.Handle); else ctx.Mover.Hide(w.Handle);
            }
            _all.Remove(orphan);
        }
        ArrangeAllInView(ctx);
    }

    /// <summary>Arranges the workspace in view on every monitor, as after a reload.</summary>
    public void ArrangeAllInView(WmContext ctx) =>
        _all.Where(w => w.InView).ToList().ForEach(w => ctx.Layouts.Arrange(ctx, w));
}
