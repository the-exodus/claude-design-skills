#!/usr/bin/env python3
"""PreToolUse hook: asks before a change to a path the repository protects.

Reads Claude Code's hook input on stdin. Prints one PreToolUse decision as JSON on
stdout, or nothing to let the call go ahead, and always exits 0. A non-zero exit
therefore means no interpreter or a crash, which the hook's `onFailure: "block"`
turns into a block; anything the script can catch ends in an `ask` that says why.

The list format is defined in the plugin's README. Python 3 standard library only.
"""

import glob
import itertools
import json
import os
import posixpath
import re
import sys

LIST = ".claude/protected-paths.txt"
FILE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}

# Words that run the next word as a command, so it is the next word that is looked at.
WRAPPERS = {"sudo", "env", "command", "builtin", "exec", "nohup", "time", "nice", "xargs",
            "then", "do", "else", "elif", "if", "while", "until", "!"}
WRITERS = {
    # POSIX
    "mv", "cp", "rm", "rmdir", "tee", "patch", "dd", "truncate",
    # PowerShell cmdlets and their aliases (Windows PowerShell 5.1's included)
    "set-content", "sc", "add-content", "ac", "out-file", "new-item", "ni",
    "copy-item", "copy", "cpi", "move-item", "move", "mi",
    "remove-item", "del", "erase", "rd", "ri",
    "rename-item", "ren", "rni", "clear-content", "clc",
}
GIT_WRITERS = {"checkout", "restore", "apply", "mv", "rm"}
CHANGE_DIRECTORY = {"cd", "pushd", "chdir", "set-location", "sl", "push-location"}
DOTNET_FILE_WRITE = re.compile(r"\[(?:system\.)?io\.file\]::(?:write|append|copy|move|delete|replace)", re.I)
NULL_TARGETS = {"/dev/null", "/dev/stdout", "/dev/stderr", "$null", "nul"}
GLOB_CHARS = re.compile(r"[*?\[]")
DRIVE = re.compile(r"^([A-Za-z]):(?:/|$)")
GIT_BASH_DRIVE = re.compile(r"^/([A-Za-z])(?=/|$)")


class Refusal(Exception):
    """Something the guard cannot check, so the call is asked about with this reason."""


def main():
    try:
        reason = decide(sys.stdin.buffer.read())
    except Refusal as refusal:
        reason = str(refusal)
    except Exception as error:  # fail closed on anything unforeseen
        reason = failure(f"{type(error).__name__}: {error}")
    if reason:
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }}))
    return 0


def failure(what):
    return (f"The guard hook could not check this call ({what}), so it asks rather than let a change "
            "to a protected path through. Author: approve only a change you have checked yourself. "
            "Agent: tell the author the guard failed, and stop.")


def protected_message(shown, why):
    return (f"{shown} is protected by this repository's guard ({why}): changing it is a provisional "
            "closure, which the author decides. Author: approve only if a provisional closure that names "
            "this path is already recorded. Agent: do not make this change another way (another tool, a "
            "shell command, a script, a copy or a move). Record a provisional closure that names this path "
            "and why the change is needed, then stop and wait for the author.")


# Paths are strings with "/" separators, absolute, optionally led by an upper-case drive ("C:/x").

def split_drive(path):
    match = DRIVE.match(path)
    if match:
        return match.group(1).upper() + ":", path[2:] or "/"
    return "", path


def norm(path):
    drive, rest = split_drive(path.replace("\\", "/"))
    if not rest:
        return drive
    rest = posixpath.normpath(rest)
    if rest.startswith("//") and not drive:
        return rest
    return drive + rest


def is_absolute(path):
    return path.startswith("/") or bool(DRIVE.match(path))


def join(base, path):
    path = path.replace("\\", "/")
    return norm(path if is_absolute(path) else base + "/" + path)


def parent(path):
    drive, rest = split_drive(path)
    return drive + posixpath.dirname(rest)


def same(a, b):
    return a.lower() == b.lower()


def under(path, root):
    path, root = path.lower(), root.lower().rstrip("/")
    return path == root or path.startswith(root + "/")


def relative(path, root):
    return path[len(root.rstrip("/")):].lstrip("/")


# The list

class Entry:
    def __init__(self, line):
        pattern = line.strip().replace("\\", "/")
        while pattern.startswith("./"):
            pattern = pattern[2:]
        pattern = pattern.strip("/").lower()
        self.pattern = pattern
        segments = pattern.split("/")
        literal = list(itertools.takewhile(lambda s: not GLOB_CHARS.search(s), segments))
        self.prefix = "/".join(literal)
        self.regex = None if len(literal) == len(segments) else re.compile(glob_regex(segments), re.S)

    def matches(self, rel):
        """Whether the entry protects rel, or rel is a directory holding paths it protects."""
        if not rel:
            return False
        if self.regex is None:
            return under(rel, self.prefix) or self.prefix.startswith(rel + "/")
        if self.regex.fullmatch(rel):
            return True
        return bool(self.prefix) and (rel == self.prefix or self.prefix.startswith(rel + "/"))


def glob_regex(segments):
    """git's :(glob) pathspec as a regex: * and ? within a segment, ** across segments."""
    out = ""
    last = len(segments) - 1
    for i, segment in enumerate(segments):
        if segment == "**":
            out += (".*" if i == last else "(?:.*/)?") if i == 0 else ("/.+" if i == last else "/(?:.*/)?")
            continue
        if i > 0 and segments[i - 1] != "**":
            out += "/"
        out += segment_regex(segment)
    return out


def segment_regex(segment):
    out, i = "", 0
    while i < len(segment):
        c = segment[i]
        if c == "*":
            out += "[^/]*"
        elif c == "?":
            out += "[^/]"
        elif c == "[" and segment.find("]", i + 2) != -1:
            negate = segment[i + 1] in "!^"
            start = i + 2 if negate else i + 1
            end = segment.find("]", start + 1)  # a "]" first in the class is part of it
            if end == -1:
                out += re.escape(c)
            else:
                body = segment[start:end].replace("\\", "\\\\").replace("[", "\\[")
                out += ("[^/" if negate else "[") + body + "]"
                i = end
        else:
            out += re.escape(c)
        i += 1
    return out


def read_list(root, cache):
    """The entries of root's list, None when there is none; Refusal when it cannot be read."""
    if root.lower() in cache:
        return cache[root.lower()]
    path = root.rstrip("/") + "/" + LIST
    try:
        with open(path, "rb") as handle:
            data = handle.read()
        text = data.decode("utf-8-sig")
    except FileNotFoundError:
        entries = None
    except (OSError, UnicodeDecodeError) as error:
        raise Refusal(
            f"The guard cannot read {path} ({type(error).__name__}: {error}), so it cannot tell which paths "
            "this repository protects, and it asks before every edit and shell command until the list is "
            "readable again. Author: approve only a change you have checked yourself. Agent: tell the "
            "author the list is unreadable, and stop.")
    else:
        entries = [Entry(line) for line in text.splitlines()
                   if line.strip() and not line.strip().startswith("#")]
    cache[root.lower()] = entries
    return entries


def root_of(path, project):
    """The root of the worktree path is in: the nearest directory holding .git, or the project."""
    directory = path
    while True:
        if same(directory, project):
            return project
        if os.path.exists(directory + "/.git"):
            return directory
        up = parent(directory)
        if up == directory:
            return None
        directory = up


# Shell commands

def scan(command, shell):
    """Split a command into simple commands (lists of words) and the targets of its redirects."""
    segments, redirects = [[]], []
    boundaries = "|;&(){}\n" + ("`" if shell == "Bash" else "")
    word, redirect, i, n = None, False, 0, len(command)

    def end_word():
        nonlocal word, redirect
        if word is not None:
            segments[-1].append(word)
            if redirect:
                redirects.append(word)
                redirect = False
        word = None

    while i < n:
        c = command[i]
        if c in "'\"":
            j = i + 1
            while j < n and command[j] != c:
                j += 2 if (c == '"' and shell == "Bash" and command[j] == "\\") else 1
            word = (word or "") + command[i + 1:j].replace('\\"', '"')
            i = j + 1
        elif c in boundaries:
            end_word()
            redirect = False
            segments.append([])
            i += 1
        elif c.isspace() or (c == "," and shell == "PowerShell"):
            end_word()
            i += 1
        elif c == "<":
            end_word()
            while i < n and command[i] == "<":
                i += 1
        elif c == ">":
            end_word()
            i += 1
            if i < n and command[i] in ">|":
                i += 1
            if i < n and command[i] == "&":
                j = i + 1
                while j < n and (command[j].isdigit() or command[j] == "-"):
                    j += 1
                if j > i + 1:  # >&2, 2>&1: duplicates a stream, writes no file
                    i = j
                    continue
                i += 1
            redirect = True
        else:
            word = (word or "") + c
            i += 1
    end_word()
    return [s for s in segments if s], redirects


def command_name(word):
    name = word.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


def command_positions(words):
    """Indexes of the words run as commands: the first after wrappers, and what find -exec runs."""
    positions, i = [], 0
    while i < len(words):
        word = words[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", word) or command_name(word) in WRAPPERS:
            i += 1
            while i < len(words) and words[i].startswith("-") and command_name(words[i - 1]) in WRAPPERS:
                i += 1
            continue
        positions.append(i)
        break
    positions += [k + 1 for k, w in enumerate(words[:-1]) if w in ("-exec", "-execdir", "-ok")]
    return positions


def writes(words, positions):
    for p in positions:
        name = command_name(words[p])
        rest = words[p + 1:]
        if name in WRITERS:
            return True
        if name in ("sed", "gsed") and any(re.match(r"^-[A-Za-z]*i|^--in-place", w) for w in rest):
            return True
        if name == "git":
            sub = [w for w in rest if not w.startswith("-")]
            if sub and sub[0].lower() in GIT_WRITERS:
                return True
    return False


def expand_home(word, home):
    for prefix in ("~", "$HOME", "${HOME}", "$env:USERPROFILE", "$env:HOME", "%USERPROFILE%"):
        if word.lower() == prefix.lower() or word.lower().startswith(prefix.lower() + "/") \
                or word.lower().startswith(prefix.lower() + "\\"):
            return home + word[len(prefix):]
    return word


def resolve(word, cwd, home, drive):
    word = expand_home(word, home).replace("\\", "/")
    if drive and GIT_BASH_DRIVE.match(word):
        word = GIT_BASH_DRIVE.sub(lambda m: m.group(1).upper() + ":", word)
    return join(cwd, word)


def shell_targets(command, shell, cwd, home, drive):
    """Whether the command writes, and every path it names, resolved."""
    segments, redirects = scan(command, shell)
    does_write = DOTNET_FILE_WRITE.search(command) is not None or any(
        command_name(t) not in NULL_TARGETS and t.lower() not in NULL_TARGETS for t in redirects)
    targets = []
    for words in segments:
        positions = command_positions(words)
        if positions and command_name(words[positions[0]]) in CHANGE_DIRECTORY:
            args = [w for w in words[positions[0] + 1:] if not w.startswith("-")]
            cwd = resolve(args[0], cwd, home, drive) if args else home
            continue
        does_write = does_write or writes(words, positions)
        for word in words:
            for candidate in path_candidates(word):
                path = resolve(candidate, cwd, home, drive)
                targets.append(path)
                if GLOB_CHARS.search(candidate):
                    targets += [norm(p) for p in itertools.islice(glob.iglob(path), 2000)]
    return does_write, targets


def path_candidates(word):
    word = re.sub(r"^-\w+:", "", word)  # -Path:x
    candidates = []
    if "=" in word:
        candidates.append(word.rsplit("=", 1)[1])
    if not word.startswith("-"):
        candidates.append(word)
    return [c for c in candidates if c and "://" not in c and not re.match(r"^\$\w+$", c)]


# The decision

def decide(raw):
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise Refusal(failure(f"its input is not JSON: {error}"))
    if not isinstance(data, dict) or not isinstance(data.get("tool_name"), str) \
            or not isinstance(data.get("tool_input"), dict):
        raise Refusal(failure("its input has no tool_name and tool_input"))
    tool, tool_input = data["tool_name"], data["tool_input"]
    if tool not in FILE_TOOLS | SHELL_TOOLS:
        return None

    cwd = norm(data["cwd"]) if isinstance(data.get("cwd"), str) and data["cwd"] else norm(os.getcwd())
    project = norm(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
    home = norm(os.path.expanduser("~"))
    drive = split_drive(project)[0] or split_drive(cwd)[0]
    user_settings = [home + "/.claude/settings.json"]
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        user_settings.append(norm(os.environ["CLAUDE_CONFIG_DIR"]) + "/settings.json")

    cache = {}
    session_roots = [project] + [r for r in [root_of(cwd, project)] if r]
    opted_in = any(read_list(root, cache) is not None for root in session_roots)

    if tool in FILE_TOOLS:
        path = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not isinstance(path, str) or not path:
            raise Refusal(failure(f"{tool} input has no file_path or notebook_path"))
        targets = [join(cwd, path)]
    else:
        command = tool_input.get("command")
        if not isinstance(command, str):
            raise Refusal(failure(f"{tool} input has no command"))
        does_write, targets = shell_targets(command, tool, cwd, home, drive)
        if not does_write:
            # Still fail closed on an unreadable list for a target's own worktree.
            for target in targets:
                root = root_of(target, project)
                if root:
                    read_list(root, cache)
            return None

    for target in targets:
        if opted_in and any(same(target, s) for s in user_settings):
            return protected_message("~/.claude/settings.json" if same(target, user_settings[0]) else target,
                                     "user settings can switch every hook off")
        root = root_of(target, project)
        if root is None:
            continue
        entries = []
        for list_root in [root] + session_roots:
            entries += read_list(list_root, cache) or []
        rel = relative(target, root)
        if any(entry.matches(rel.lower()) for entry in entries):
            return protected_message(rel, LIST)
    return None


if __name__ == "__main__":
    sys.exit(main())
