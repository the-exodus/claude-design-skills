namespace Tessera.Rules;

/// <summary>When a rule is applied.</summary>
public enum RuleTrigger
{
    /// <summary>When the window opens. The default.</summary>
    Open,

    /// <summary>Whenever the title of a managed window changes.</summary>
    TitleChange,
}

/// <summary>What a rule says to do with a window it matches.</summary>
public enum RuleAction
{
    /// <summary>Give the window a tile. The default.</summary>
    Tile,

    /// <summary>Make it a floating window: managed, on a workspace, but without a tile.</summary>
    Float,

    /// <summary>Leave the window unmanaged: on no workspace, touched by no command.</summary>
    Ignore,
}

/// <summary>
/// One [[rule]] block of the config file, exactly as the user wrote it. Holds values only;
/// matching is done elsewhere.
/// </summary>
public sealed record Rule
{
    /// <summary>Executable name to match, or null to match any.</summary>
    public string? Process { get; init; }

    /// <summary>Window class name to match, or null to match any.</summary>
    public string? Class { get; init; }

    /// <summary>Text the window title must contain, or null to match any.</summary>
    public string? Title { get; init; }

    /// <summary>When the rule is applied.</summary>
    public RuleTrigger On { get; init; } = RuleTrigger.Open;

    /// <summary>What to do with a matching window.</summary>
    public RuleAction Action { get; init; } = RuleAction.Tile;

    /// <summary>Number of the workspace to place the window on, or null for the one in view.</summary>
    public int? Workspace { get; init; }
}
