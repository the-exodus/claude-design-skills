# guard

A PreToolUse hook that makes a change to a repository's protected paths, such as its architecture tests, reach the author. Changing one is a provisional closure: the author decides it, not the build.

## What it does

- On every Edit, Write, NotebookEdit, Bash and PowerShell call, it reads the repository's list, `.claude/protected-paths.txt`. A call that would change a listed path gets `ask`, with a message: the path is protected; the author approves only if a provisional closure naming it is already recorded; the agent does not try another way, records a closure naming the path, and stops.
- Every protected change asks. No approval carries over to the next one.
- Headless (`-p`), nobody can answer an `ask`: the call is denied and the agent reads the message in the tool result.
- Edit, Write and NotebookEdit are matched on the file they name. Bash and PowerShell are matched on the command's text, best effort: a command asks when it names a protected path and contains a write (a redirect to a file, `sed -i`, `tee`, `mv`, `cp`, `rm`, `git checkout|restore|apply|mv|rm`, `patch`, `dd`, `truncate`; `Set-Content`, `Add-Content`, `Out-File`, `New-Item`, `Copy-Item`, `Move-Item`, `Remove-Item`, `Rename-Item`, `Clear-Content` and their aliases, `[IO.File]::Write*`). A test run or a read that names the path goes ahead.
- Fixed rule, in a repository that has a list: writes to the user's `~/.claude/settings.json` (and `$CLAUDE_CONFIG_DIR/settings.json`) ask too, since user settings can switch every hook off and no repository-relative list can name them.
- An absent list means the repository has not opted in: everything goes ahead.
- It fails closed. An unreadable list, input it cannot parse, or an error in the hook ends in `ask` saying why; no interpreter, a crash or a timeout blocks the call (`onFailure: "block"`).

## The list

`.claude/protected-paths.txt`, at the repository root. Entries are git's `:(glob,icase)` pathspecs:

- One entry per line, relative to the repository root, with `/` separators. A `\` is read as `/`; a leading `/` or `./` is ignored.
- Blank lines, and lines whose first non-blank character is `#`, are ignored. There are no comments after an entry.
- A plain path, with no `*`, `?` or `[`, is that file, or that directory and everything below it. A trailing `/` changes nothing.
- `*` matches any characters within one path segment, `?` one character, `[abc]` one character of the set, `[!abc]` one not in it. None of them matches `/`.
- `**` as a whole segment matches across segments, zero included: `**/Directory.Build.props` is that file at any depth, the root's included; `dir/**` is everything below `dir`; `a/**/b` allows any directories between. `**` inside a segment is `*`.
- No braces: write one line per alternative.
- Matching ignores case.

A path is resolved against the root of the worktree it is in: the nearest enclosing directory holding `.git`, or the project directory. The entries that apply are that worktree's list and the project's. For a shell command, a directory that holds a protected path counts as protected (`rm -r tests` when `tests/test_architecture.py` is listed).

```
# Architecture tests: the rules and what they declare
tests/architecture/**
# What builds and runs them
**/Directory.Build.props
# The guard itself
.claude/protected-paths.txt
.claude/settings.json
.claude/settings.local.json
```

## Opting a repository in

The plugin is installed like the marketplace's others (`claude plugin install guard@claude-design-skills`), but it is a repository that opts in:

1. Enable the plugin in the project's `.claude/settings.json`, and set the two keys beside it:

   ```json
   {
     "enabledPlugins": { "guard@claude-design-skills": true },
     "permissions": { "disableBypassPermissionsMode": "disable" },
     "disableAllHooks": false
   }
   ```

   `disableBypassPermissionsMode` because whether a hook's `ask` prompts under bypassPermissions is not documented, and that mode would let the agent edit `.claude/` unasked; a local settings file cannot undo it. `"disableAllHooks": false` because project settings override user settings, so a `true` in the user's file does not switch the guard off here.

2. Write `.claude/protected-paths.txt` naming the architecture tests and what decides how they run, the list itself, `.claude/settings.json` and `.claude/settings.local.json`. The local settings file is usually untracked, so the guard is the only thing that sees a change to it.

## Requirements

- Claude Code 2.1.295 or later, for `onFailure`.
- Python 3, found as `python3`, `python` or `py -3`, in that order. Standard library only.
- On Windows without Git Bash, hooks run in PowerShell, and the fallback chain needs pwsh 7: Windows PowerShell 5.1 has no `||`.

## Gaps

What the hook cannot see. The review cycle's traceability check is the backstop for all of them.

- A script, test or build step that opens and writes a file itself.
- A nested `claude` started through Bash with its own `--settings`, which can set `disableAllHooks`.
- `claude --bare`, which loads no plugin hooks.
- A shell command that builds the path at run time (a variable, a generated name), where the text never names it.
