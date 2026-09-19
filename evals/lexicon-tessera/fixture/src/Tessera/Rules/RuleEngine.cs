using System;
using Tessera.Workspaces;

namespace Tessera.Rules;

/// <summary>What is known about a window at the moment rules are matched against it.</summary>
public sealed record WindowFacts(string Process, string Class, string Title);

/// <summary>
/// Matches windows against the user's rules. Rules are read in file order and the first
/// match for the trigger at hand wins.
/// </summary>
public sealed class RuleEngine
{
    /// <summary>
    /// Returns the first rule with the given trigger that matches, or null when none does.
    /// </summary>
    public Rule? FirstMatch(WmContext ctx, WindowFacts facts, RuleTrigger trigger)
    {
        foreach (var rule in ctx.Config.Rules)
        {
            if (rule.On == trigger && Matches(rule, facts))
                return rule;
        }
        return null;
    }

    /// <summary>
    /// Called when the title of a managed window changes. Re-applies the rules whose
    /// trigger is <see cref="RuleTrigger.TitleChange"/>, so a window that only gets its
    /// real title after opening can still be floated, tiled or released.
    /// </summary>
    public void OnTitleChanged(WmContext ctx, ManagedWindow window, string newTitle)
    {
        window.Title = newTitle;
        var facts = new WindowFacts(window.Process, window.Class, newTitle);
        var rule = FirstMatch(ctx, facts, RuleTrigger.TitleChange);
        if (rule is null)
            return;

        var workspace = ctx.Workspaces.WorkspaceOf(window);
        switch (rule.Action)
        {
            case RuleAction.Ignore:
                // Released: from here on the window is unmanaged and is not watched again.
                workspace.Remove(window);
                ctx.Unmanaged.Add(window.Handle);
                if (ctx.Focused == window) ctx.Focused = null;
                break;
            case RuleAction.Float when window.Mode == WindowMode.Tiled:
                window.FloatBounds = ctx.Mover.BoundsOf(window.Handle);
                window.Mode = WindowMode.Floating;
                break;
            case RuleAction.Tile when window.Mode == WindowMode.Floating:
                window.Mode = WindowMode.Tiled;
                break;
            default:
                return;
        }
        ctx.Layouts.Arrange(ctx, workspace);
    }

    /// <summary>
    /// True when every field the rule gives matches. Plain comparisons only: this runs on
    /// every title change of every managed window.
    /// </summary>
    private static bool Matches(Rule rule, WindowFacts facts)
    {
        if (rule.Process is not null &&
            !string.Equals(rule.Process, facts.Process, StringComparison.OrdinalIgnoreCase))
            return false;
        if (rule.Class is not null && rule.Class != facts.Class)
            return false;
        if (rule.Title is not null &&
            !facts.Title.Contains(rule.Title, StringComparison.Ordinal))
            return false;
        return true;
    }
}
