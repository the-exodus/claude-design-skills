using System;
using System.Collections.Generic;

namespace Tessera.Layouts;

/// <summary>
/// The main-stack layout: the first window takes the main tile on the left and the other
/// windows share the stack on the right. The main tile's width is the split ratio
/// (lexicon: split ratio) times the width of the work area, less half a gutter.
/// </summary>
public sealed class MainStackLayout : ILayout
{
    public string Name => "main-stack";

    /// <inheritdoc />
    public IReadOnlyList<Rect> Arrange(LayoutInput input)
    {
        if (input.Count == 0)
            return Array.Empty<Rect>();

        var area = input.WorkArea;
        if (input.Count == 1)
            return new[] { area };

        int mainWidth = (int)Math.Round(area.Width * input.SplitRatio) - input.Gutter / 2;
        var main = new Rect(area.X, area.Y, mainWidth, area.Height);

        int restX = main.Right + input.Gutter;
        var rest = new Rect(restX, area.Y, area.Right - restX, area.Height);

        var tiles = new List<Rect>(input.Count) { main };
        tiles.AddRange(SecondaryArea.Rows(rest, input.Count - 1, input.Gutter));
        return tiles;
    }
}

/// <summary>
/// The stack of the main-stack layout: the part of the work area beside the main tile,
/// cut into equal rows, one per window. Called SecondaryArea because a type named Stack
/// reads as the collection.
/// </summary>
internal static class SecondaryArea
{
    /// <summary>
    /// Cuts <paramref name="area"/> into <paramref name="count"/> rows of equal height with
    /// <paramref name="gutter"/> pixels between them. Pixels that do not divide evenly go
    /// to the last row so the rows always reach the bottom of the area.
    /// </summary>
    public static IEnumerable<Rect> Rows(Rect area, int count, int gutter)
    {
        int usable = area.Height - gutter * (count - 1);
        int height = usable / count;
        int y = area.Y;

        for (int i = 0; i < count; i++)
        {
            bool last = i == count - 1;
            int h = last ? area.Bottom - y : height;
            yield return new Rect(area.X, y, area.Width, h);
            y += h + gutter;
        }
    }
}
