"""Pipes PreToolUse input into the guard plugin's hook and reads its decision.

    python3 -m unittest discover -s evals/guard

Free, no model involved. Each test builds a repository in a temporary directory,
runs plugins/guard/hooks/guard.py as Claude Code would (JSON on stdin), and checks
that it exits 0 and either prints nothing (the call goes ahead) or prints one
PreToolUse `ask` decision.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / "plugins" / "guard" / "hooks" / "guard.py"

LIST = """\
# Architecture tests, and the files that decide how they run
tests/architecture/**
tests/test_architecture.py
**/Directory.Build.props
build/
scripts/*.sh
src/Rules?.cs

# The guard's own settings
.claude/protected-paths.txt
.claude/settings.json
.claude/settings.local.json
# docs/adr/**
"""


def make_repo(root, protected=LIST, git_file=False):
    """A repository at root: a .git (directory, or a worktree's file) and the list."""
    root.mkdir(parents=True, exist_ok=True)
    if git_file:
        (root / ".git").write_text("gitdir: /elsewhere/.git/worktrees/x\n")
    else:
        (root / ".git").mkdir()
    (root / "tests").mkdir()
    (root / "tests" / "test_architecture.py").write_text("ALLOWED = {}\n")
    (root / "tests" / "test_report.py").write_text("\n")
    (root / "src").mkdir()
    if protected is not None:
        (root / ".claude").mkdir()
        (root / ".claude" / "protected-paths.txt").write_text(protected, encoding="utf-8")
    return root


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="guard-test-"))
        self.home = self.tmp / "home"
        (self.home / ".claude").mkdir(parents=True)
        self.repo = make_repo(self.tmp / "repo")

    def tearDown(self):
        for path in self.tmp.rglob("*"):
            if not path.is_symlink():
                path.chmod(0o755)
        shutil.rmtree(self.tmp)

    def run_guard(self, tool, tool_input, cwd=None, project=None, stdin=None, env=None, run_in=None):
        payload = {
            "session_id": "test",
            "transcript_path": "/dev/null",
            "cwd": str(cwd if cwd is not None else self.repo),
            "permission_mode": "dontAsk",
            "hook_event_name": "PreToolUse",
            "tool_name": tool,
            "tool_input": tool_input,
            "tool_use_id": "toolu_test",
        }
        full_env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR")}
        full_env["HOME"] = str(self.home)
        full_env["USERPROFILE"] = str(self.home)
        full_env["CLAUDE_PROJECT_DIR"] = str(project if project is not None else self.repo)
        full_env.update(env or {})
        result = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps(payload) if stdin is None else stdin,
            capture_output=True, text=True, env=full_env, cwd=run_in or self.tmp, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def assertAsks(self, out, mentions=None):
        self.assertTrue(out.strip(), "expected an ask decision, got none")
        decision = json.loads(out)
        specific = decision["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PreToolUse")
        self.assertEqual(specific["permissionDecision"], "ask")
        if mentions:
            self.assertIn(mentions.lower(), specific["permissionDecisionReason"].lower())
        return specific["permissionDecisionReason"]

    def assertAllows(self, out):
        self.assertEqual(out.strip(), "", "expected no decision")

    def write(self, rel, **kw):
        return self.run_guard("Write", {"file_path": str(self.repo / rel), "content": "x"}, **kw)

    def bash(self, command, **kw):
        return self.run_guard("Bash", {"command": command, "description": "d"}, **kw)

    def pwsh(self, command, **kw):
        return self.run_guard("PowerShell", {"command": command}, **kw)


class FileTools(GuardTest):
    def test_write_to_a_protected_file_asks_with_the_message(self):
        reason = self.assertAsks(self.write("tests/test_architecture.py"), "tests/test_architecture.py")
        self.assertIn("provisional closure", reason)
        self.assertIn("stop", reason)

    def test_edit_to_a_protected_file_asks(self):
        out = self.run_guard("Edit", {"file_path": str(self.repo / "tests/test_architecture.py"),
                                      "old_string": "{}", "new_string": "{1}"})
        self.assertAsks(out)

    def test_notebook_edit_reads_notebook_path(self):
        out = self.run_guard("NotebookEdit", {"notebook_path": str(self.repo / "tests/architecture/rules.ipynb"),
                                              "new_source": "x"})
        self.assertAsks(out)

    def test_unprotected_file_goes_ahead(self):
        self.assertAllows(self.write("src/app.py"))
        self.assertAllows(self.write("tests/test_report.py"))

    def test_other_tools_go_ahead(self):
        self.assertAllows(self.run_guard("Read", {"file_path": str(self.repo / "tests/test_architecture.py")}))


class ListSemantics(GuardTest):
    def test_double_star_prefix_matches_the_root_file(self):
        self.assertAsks(self.write("Directory.Build.props"))

    def test_double_star_prefix_matches_at_depth(self):
        self.assertAsks(self.write("src/a/b/Directory.Build.props"))
        self.assertAllows(self.write("src/Directory.Build.targets"))

    def test_trailing_double_star_covers_the_whole_directory(self):
        self.assertAsks(self.write("tests/architecture/rules.py"))
        self.assertAsks(self.write("tests/architecture/deep/er/rules.py"))
        self.assertAllows(self.write("tests/architecture_notes.md"))

    def test_plain_directory_entry_covers_everything_below(self):
        self.assertAsks(self.write("build/props/common.props"))
        self.assertAllows(self.write("buildtools/x"))

    def test_star_stays_within_a_segment(self):
        self.assertAsks(self.write("scripts/release.sh"))
        self.assertAllows(self.write("scripts/sub/release.sh"))

    def test_question_mark_is_one_character(self):
        self.assertAsks(self.write("src/Rules1.cs"))
        self.assertAllows(self.write("src/Rules12.cs"))
        self.assertAllows(self.write("src/a/Rules1.cs"))

    def test_bracket_is_one_character_of_a_set(self):
        (self.repo / ".claude/protected-paths.txt").write_text("src/[ab]x.cs\nsrc/[!ab]y.cs\n")
        self.assertAsks(self.write("src/ax.cs"))
        self.assertAllows(self.write("src/cx.cs"))
        self.assertAsks(self.write("src/cy.cs"))
        self.assertAllows(self.write("src/ay.cs"))

    def test_matching_ignores_case(self):
        self.assertAsks(self.write("TESTS/Test_Architecture.PY"))
        self.assertAsks(self.write("directory.build.props"))

    def test_comments_and_blank_lines_protect_nothing(self):
        self.assertAllows(self.write("docs/adr/0001-x.md"))

    def test_the_list_protects_itself_and_the_settings(self):
        self.assertAsks(self.write(".claude/protected-paths.txt"))
        self.assertAsks(self.write(".claude/settings.local.json"))

    def test_backslashes_in_the_list_are_separators(self):
        (self.repo / ".claude/protected-paths.txt").write_text("tests\\architecture\\**\n")
        self.assertAsks(self.write("tests/architecture/rules.py"))


class WindowsPaths(GuardTest):
    """Windows paths, run on any platform.

    On Linux a "C:" is an ordinary directory name, so the repository is built at
    C:/repo relative to the guard's working directory: the guard reads C:/repo/...
    and finds it there, while still being handed the paths exactly as Claude Code
    on Windows hands them (file paths with backslashes; CLAUDE_PROJECT_DIR as
    C:/... under Git Bash and C:\\... under pwsh).
    """

    def setUp(self):
        super().setUp()
        if os.name == "nt":
            self.skipTest("the C: trick needs a POSIX file system")
        make_repo(self.tmp / "C:" / "repo")

    def test_backslash_file_path_with_either_project_dir_form(self):
        for project in ("C:/repo", "C:\\repo"):
            with self.subTest(project=project):
                out = self.run_guard("Write", {"file_path": "C:\\repo\\tests\\test_architecture.py", "content": "x"},
                                     cwd="C:\\repo", project=project)
                self.assertAsks(out, "tests/test_architecture.py")

    def test_drive_letter_case_and_unprotected_file(self):
        out = self.run_guard("Edit", {"file_path": "c:\\REPO\\Directory.Build.props"}, cwd="C:\\repo", project="C:\\repo")
        self.assertAsks(out)
        out = self.run_guard("Edit", {"file_path": "C:\\repo\\src\\app.cs"}, cwd="C:\\repo", project="C:\\repo")
        self.assertAllows(out)

    def test_powershell_relative_path_with_backslashes(self):
        out = self.run_guard("PowerShell", {"command": "Set-Content -Path tests\\test_architecture.py -Value 'x'"},
                             cwd="C:\\repo", project="C:/repo")
        self.assertAsks(out)

    def test_git_bash_drive_path_in_a_command(self):
        out = self.run_guard("Bash", {"command": "sed -i 's/a/b/' /c/repo/tests/test_architecture.py"},
                             cwd="C:\\repo", project="C:/repo")
        self.assertAsks(out)


class ShellCommands(GuardTest):
    def test_posix_writes_naming_a_protected_path_ask(self):
        commands = [
            "sed -i 's/set()/{\"gaugefeed.stations\"}/' tests/test_architecture.py",
            "sed -i.bak -e 's/a/b/' tests/test_architecture.py",
            "echo x > tests/test_architecture.py",
            "printf 'x' >> tests/test_architecture.py",
            "cat new.py | tee tests/test_architecture.py",
            "cp /tmp/new.py tests/test_architecture.py",
            "mv tests/test_architecture.py /tmp/old.py",
            "rm -rf tests/architecture",
            "rm -r tests",
            "git checkout -- tests/test_architecture.py",
            "git restore tests/test_architecture.py",
            "git apply widen.patch && git diff tests/test_architecture.py",
            "patch tests/test_architecture.py < widen.diff",
            "dd if=/tmp/new.py of=tests/test_architecture.py",
            "truncate -s 0 tests/test_architecture.py",
            "cd tests && sed -i 's/a/b/' test_architecture.py",
            "sed -i 's/a/b/' tests/*.py",
            f"sed -i 's/a/b/' {self.repo}/tests/test_architecture.py",
            "sed -i 's/a/b/' \"tests/test_architecture.py\"",
            "sed -i 's/a/b/' \"$CLAUDE_PROJECT_DIR/tests/test_architecture.py\"",
            "cat > Directory.Build.props <<'EOF'\n<Project/>\nEOF",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertAsks(self.bash(command))

    def test_pwsh_writes_naming_a_protected_path_ask(self):
        commands = [
            "Set-Content -Path tests/test_architecture.py -Value 'x'",
            "Add-Content tests/test_architecture.py 'x'",
            "'x' | Out-File -FilePath tests/test_architecture.py",
            "New-Item -ItemType File -Force tests/architecture/rules.py",
            "ni tests/architecture/rules.py -Force",
            "Copy-Item new.py tests/test_architecture.py",
            "copy new.py tests\\test_architecture.py",
            "cpi new.py tests/test_architecture.py",
            "Move-Item tests/test_architecture.py old.py",
            "mi tests/test_architecture.py old.py",
            "Remove-Item -Recurse tests/architecture",
            "del tests\\test_architecture.py",
            "ri tests/test_architecture.py",
            "erase tests/test_architecture.py",
            "[IO.File]::WriteAllText('tests/test_architecture.py', 'x')",
            "[System.IO.File]::AppendAllLines(\"tests/test_architecture.py\", $lines)",
            "(Get-Content tests/test_architecture.py) -replace 'a','b' | Set-Content tests/test_architecture.py",
            "'x' > tests/test_architecture.py",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertAsks(self.pwsh(command))

    def test_test_runs_and_reads_naming_a_protected_path_go_ahead(self):
        commands = [
            "python3 -m unittest tests/test_architecture.py",
            "python3 -m pytest tests/test_architecture.py 2>&1 | tail -20",
            "python3 -m unittest discover -s tests > /dev/null 2>&1",
            "cat tests/test_architecture.py",
            "sed -n '1,40p' tests/test_architecture.py",
            "grep -n ALLOWED tests/test_architecture.py",
            "git diff -- tests/test_architecture.py",
            "git log --oneline -- tests/architecture",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertAllows(self.bash(command))
        for command in ["Get-Content tests\\test_architecture.py",
                        "python -m unittest tests\\test_architecture.py 2>&1 | Select-Object -Last 20",
                        "Select-String -Path tests/test_architecture.py -Pattern ALLOWED > $null"]:
            with self.subTest(command=command):
                self.assertAllows(self.pwsh(command))

    def test_writes_to_unprotected_paths_go_ahead(self):
        self.assertAllows(self.bash("sed -i 's/a/b/' src/app.py"))
        self.assertAllows(self.bash("echo x > tests/test_report.py"))
        self.assertAllows(self.pwsh("Set-Content src/app.py 'x'"))


class Failures(GuardTest):
    def test_absent_list_means_not_opted_in(self):
        (self.repo / ".claude/protected-paths.txt").unlink()
        self.assertAllows(self.write("tests/test_architecture.py"))
        self.assertAllows(self.bash("sed -i 's/a/b/' tests/test_architecture.py"))
        self.assertAllows(self.run_guard("Write", {"file_path": str(self.home / ".claude/settings.json")}))

    def test_unreadable_list_blocks(self):
        listed = self.repo / ".claude/protected-paths.txt"
        listed.unlink()
        listed.mkdir()
        self.assertAsks(self.write("src/app.py"), "protected-paths.txt")

    def test_list_without_read_permission_blocks(self):
        if os.name == "nt" or os.geteuid() == 0:
            self.skipTest("needs a non-root POSIX user")
        (self.repo / ".claude/protected-paths.txt").chmod(0)
        self.assertAsks(self.write("src/app.py"), "protected-paths.txt")

    def test_list_that_is_not_text_blocks(self):
        (self.repo / ".claude/protected-paths.txt").write_bytes(b"tests/\xff\xfe\n")
        self.assertAsks(self.write("src/app.py"))

    def test_malformed_input_blocks(self):
        for stdin in ["", "not json", "[1, 2]", '{"tool_name": "Write", "tool_input": "x"}']:
            with self.subTest(stdin=stdin):
                self.assertAsks(self.run_guard("Write", {}, stdin=stdin))


class UserSettings(GuardTest):
    def test_user_settings_are_guarded_in_a_repository_with_a_list(self):
        self.assertAsks(self.run_guard("Write", {"file_path": str(self.home / ".claude/settings.json"), "content": "{}"}))
        self.assertAsks(self.bash("echo '{\"disableAllHooks\": true}' > ~/.claude/settings.json"))
        self.assertAsks(self.bash("jq '.disableAllHooks=true' x > $HOME/.claude/settings.json"))
        self.assertAsks(self.pwsh("Set-Content $env:USERPROFILE\\.claude\\settings.json '{}'"))
        self.assertAllows(self.run_guard("Write", {"file_path": str(self.home / ".claude/notes.md")}))

    def test_claude_config_dir_is_guarded_too(self):
        config = self.tmp / "config"
        config.mkdir()
        out = self.run_guard("Edit", {"file_path": str(config / "settings.json")}, env={"CLAUDE_CONFIG_DIR": str(config)})
        self.assertAsks(out)


class Worktrees(GuardTest):
    def test_worktree_inside_the_project_uses_its_own_root(self):
        worktree = make_repo(self.repo / ".claude/worktrees/wt", git_file=True)
        self.assertAsks(self.run_guard("Write", {"file_path": str(worktree / "tests/test_architecture.py")}, cwd=worktree))
        self.assertAllows(self.run_guard("Write", {"file_path": str(worktree / "src/app.py")}, cwd=worktree))

    def test_worktree_without_its_own_list_uses_the_project_list(self):
        worktree = make_repo(self.repo / ".claude/worktrees/wt", protected=None, git_file=True)
        self.assertAsks(self.run_guard("Write", {"file_path": str(worktree / "tests/test_architecture.py")}))

    def test_worktree_outside_the_project_in_a_shell_command(self):
        worktree = make_repo(self.tmp / "repo-wt", git_file=True)
        self.assertAsks(self.bash("sed -i 's/a/b/' tests/test_architecture.py", cwd=worktree))
        self.assertAllows(self.bash("sed -i 's/a/b/' src/app.py", cwd=worktree))


if __name__ == "__main__":
    unittest.main()
