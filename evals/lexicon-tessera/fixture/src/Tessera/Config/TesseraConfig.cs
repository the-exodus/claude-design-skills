using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Tessera.Rules;
using Tomlyn;
using Tomlyn.Model;

namespace Tessera.Config;

/// <summary>Thrown when the config file cannot be read or holds a value out of range.</summary>
public sealed class ConfigException : Exception
{
    public ConfigException(string message) : base(message) { }
}

/// <summary>
/// The user's settings, as read from tessera.toml. Immutable: a reload builds a new one.
/// </summary>
public sealed class TesseraConfig
{
    /// <summary>
    /// Name of the layout a workspace starts in: "main-stack" or "columns".
    /// This default has history; ask before changing it.
    /// </summary>
    public string DefaultLayout { get; init; } = "main-stack";

    /// <summary>The split ratio a workspace starts with, between 0.1 and 0.9.</summary>
    public double SplitRatio { get; init; } = 0.55;

    /// <summary>How far grow-main and shrink-main change the split ratio.</summary>
    public double SplitStep { get; init; } = 0.05;

    /// <summary>Pixels left empty between neighbouring tiles.</summary>
    public int Gutter { get; init; } = 8;

    /// <summary>Key combination to command text, as written under [shortcuts].</summary>
    public IReadOnlyDictionary<string, string> Shortcuts { get; init; } =
        new Dictionary<string, string>();

    /// <summary>The user's rules, in file order. The first match wins.</summary>
    public IReadOnlyList<Rule> Rules { get; init; } = Array.Empty<Rule>();

    /// <summary>Reads and validates the config file.</summary>
    /// <exception cref="ConfigException">The file is missing, malformed or out of range.</exception>
    public static TesseraConfig Load(string path)
    {
        TomlTable table;
        try
        {
            table = Toml.ToModel(File.ReadAllText(path));
        }
        catch (Exception e) when (e is IOException or TomlException)
        {
            throw new ConfigException($"{path}: {e.Message}");
        }

        var config = new TesseraConfig
        {
            DefaultLayout = table.TryGetValue("default_layout", out var l) ? (string)l : "main-stack",
            SplitRatio = table.TryGetValue("split_ratio", out var r) ? Convert.ToDouble(r) : 0.55,
            SplitStep = table.TryGetValue("split_step", out var s) ? Convert.ToDouble(s) : 0.05,
            Gutter = table.TryGetValue("gutter", out var g) ? Convert.ToInt32(g) : 8,
            Shortcuts = table.TryGetValue("shortcuts", out var k)
                ? ((TomlTable)k).ToDictionary(p => p.Key, p => (string)p.Value)
                : new Dictionary<string, string>(),
            Rules = table.TryGetValue("rule", out var rules)
                ? ((TomlTableArray)rules).Select(ReadRule).ToList()
                : new List<Rule>(),
        };

        if (config.DefaultLayout is not ("main-stack" or "columns"))
            throw new ConfigException($"default_layout: unknown layout \"{config.DefaultLayout}\"");
        if (config.SplitRatio is < 0.1 or > 0.9)
            throw new ConfigException("split_ratio must be between 0.1 and 0.9");
        if (config.Gutter < 0)
            throw new ConfigException("gutter cannot be negative");
        return config;
    }

    /// <summary>
    /// Re-reads the file and puts the result in force. On failure the old settings stay
    /// and the error is returned for the notification-area balloon.
    /// </summary>
    public static string? Reload(WmContext ctx, string path)
    {
        try
        {
            ctx.Config = Load(path);
            ctx.Workspaces.ArrangeAllInView(ctx);
            return null;
        }
        catch (ConfigException e)
        {
            ctx.Log($"reload failed: {e.Message}");
            return e.Message;
        }
    }

    private static Rule ReadRule(TomlTable t)
    {
        string? Text(string key) => t.TryGetValue(key, out var v) ? (string)v : null;

        if (Text("process") is null && Text("class") is null && Text("title") is null)
            throw new ConfigException("a rule needs at least one of process, class and title");

        return new Rule
        {
            Process = Text("process"),
            Class = Text("class"),
            Title = Text("title"),
            On = Text("on") == "title" ? RuleTrigger.TitleChange : RuleTrigger.Open,
            Action = Enum.Parse<RuleAction>(Text("action") ?? "tile", ignoreCase: true),
            Workspace = t.TryGetValue("workspace", out var n) ? Convert.ToInt32(n) : null,
        };
    }
}
