using System.Collections.Generic;

namespace Tessera.Layouts;

/// <summary>A rectangle in screen pixels.</summary>
public readonly record struct Rect(int X, int Y, int Width, int Height)
{
    public int Right => X + Width;

    public int Bottom => Y + Height;

    /// <summary>True when the rectangle encloses no pixels.</summary>
    public bool IsEmpty => Width <= 0 || Height <= 0;
}

/// <summary>
/// Everything a layout is allowed to know. There is deliberately no window handle here
/// and no WmContext: a layout cannot reach the running system.
/// </summary>
/// <param name="Count">Number of tiled windows on the workspace.</param>
/// <param name="WorkArea">The monitor's work area.</param>
/// <param name="SplitRatio">The workspace's split ratio.</param>
/// <param name="Gutter">Pixels to leave between neighbouring tiles.</param>
public readonly record struct LayoutInput(int Count, Rect WorkArea, double SplitRatio, int Gutter);

/// <summary>
/// A way of cutting a work area into tiles. Implementations are pure: the same input
/// always gives the same tiles, and nothing is kept between calls.
/// </summary>
public interface ILayout
{
    /// <summary>The name users write in the config file, such as "main-stack".</summary>
    string Name { get; }

    /// <summary>
    /// Returns one tile per tiled window, in window order. The tiles never overlap and
    /// leave <see cref="LayoutInput.Gutter"/> pixels between neighbours, with no gutter
    /// at the edge of the work area. When a workspace holds a single window, every
    /// layout gives it the whole work area. For a count of zero the result is empty.
    /// </summary>
    IReadOnlyList<Rect> Arrange(LayoutInput input);
}
