using System;
using System.Collections.Generic;
using System.Linq;
using Tessera.Workspaces;

namespace Tessera.Layouts;

/// <summary>
/// Arranges workspaces (lexicon: LayoutEngine). Asks the workspace's layout for rectangles
/// and hands them to the WindowMover, which repositions all the windows in a single batch.
/// </summary>
public sealed class LayoutEngine
{
    private readonly List<ILayout> _layouts = new()
    {
        new MainStackLayout(),
        new ColumnsLayout(),
    };

    /// <summary>Finds a layout by the name users write in the config file.</summary>
    /// <exception cref="ArgumentException">No layout has that name.</exception>
    public ILayout Get(string name) =>
        _layouts.FirstOrDefault(l => l.Name == name)
        ?? throw new ArgumentException($"unknown layout \"{name}\"", nameof(name));

    /// <summary>The layout that cycle-layout switches to from <paramref name="current"/>.</summary>
    public ILayout Next(ILayout current)
    {
        int i = _layouts.IndexOf(current);
        return _layouts[(i + 1) % _layouts.Count];
    }

    /// <summary>
    /// Puts every window of the workspace where it belongs. Does nothing for a workspace
    /// that is not in view, since its windows are hidden; it is arranged when it next
    /// comes into view.
    /// </summary>
    public void Arrange(WmContext ctx, Workspace workspace)
    {
        if (!workspace.InView)
            return;

        var tiled = workspace.Tiled.ToList();
        var input = new LayoutInput(
            tiled.Count,
            workspace.Monitor.WorkArea,
            workspace.SplitRatio,
            ctx.Config.Gutter);
        var tiles = workspace.Layout.Arrange(input);

        var placements = new List<(IntPtr, Rect)>(workspace.Windows.Count);
        for (int i = 0; i < tiled.Count; i++)
            placements.Add((tiled[i].Handle, tiles[i]));

        // Floating windows go last so that they end up above the tiles.
        foreach (var w in workspace.Windows.Where(w => w.Mode == WindowMode.Floating))
            placements.Add((w.Handle, w.FloatBounds));

        ctx.Mover.Apply(placements);
    }
}
