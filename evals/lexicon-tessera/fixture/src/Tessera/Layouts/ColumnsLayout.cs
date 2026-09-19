using System;
using System.Collections.Generic;

namespace Tessera.Layouts;

/// <summary>
/// The columns layout: every tiled window gets a column of equal width, left to right in
/// window order. There is no main tile, and the split ratio is not used.
/// </summary>
public sealed class ColumnsLayout : ILayout
{
    public string Name => "columns";

    /// <inheritdoc />
    public IReadOnlyList<Rect> Arrange(LayoutInput input)
    {
        if (input.Count == 0)
            return Array.Empty<Rect>();

        var area = input.WorkArea;
        int usable = area.Width - input.Gutter * (input.Count - 1);
        int width = usable / input.Count;

        var tiles = new List<Rect>(input.Count);
        int x = area.X;
        for (int i = 0; i < input.Count; i++)
        {
            // The last column takes the pixels that did not divide evenly, so the
            // columns always reach the right edge of the work area.
            bool last = i == input.Count - 1;
            int w = last ? area.Right - x : width;
            tiles.Add(new Rect(x, area.Y, w, area.Height));
            x += w + input.Gutter;
        }
        return tiles;
    }

    /// <summary>
    /// The narrowest a column may get before windows start refusing the size they are
    /// given. Used by the notification-area warning, not by <see cref="Arrange"/>.
    /// </summary>
    public const int MinimumUsefulWidth = 320;
}
