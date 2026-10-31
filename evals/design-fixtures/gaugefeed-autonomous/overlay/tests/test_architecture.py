"""Checks what each of gaugefeed's modules may import, and which may read files or the clock."""

import ast
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "gaugefeed"

NETWORK_ADR = "docs/adr/0001-only-the-fetcher-talks-to-the-network.md"
REPORT_ADR = "docs/adr/0002-the-report-is-built-from-readings-alone.md"
NO_STATE_ADR = "docs/adr/0003-each-cycle-is-a-fresh-process-that-keeps-no-state.md"
ARCHIVE_ADR = "docs/adr/0004-the-archive-is-packed-from-logger-dumps-alone.md"

# Every module in the package, everything it may import (standard library and
# gaugefeed modules alike, by top-level name for the standard library), and the
# decision record that drew that list (None where nobody decided it). Anything
# not listed fails, so a new dependency is a visible change.
ALLOWED = {
    "gaugefeed": (set(), None),
    "gaugefeed.__main__": (
        {"sys", "datetime", "gaugefeed.stations", "gaugefeed.fetcher", "gaugefeed.report"},
        None,
    ),
    "gaugefeed.stations": (set(), None),
    "gaugefeed.fetcher": ({"json", "urllib"}, NETWORK_ADR),
    "gaugefeed.report": ({"json", "datetime"}, REPORT_ADR),
    "gaugefeed.archive": ({"csv", "json", "sys", "pathlib", "gaugefeed.fetcher"}, ARCHIVE_ADR),
}

# The only module of the cycle that may call open(), and why: the report reads
# no files (ADR-0002) and no cycle keeps anything for the next (ADR-0003).
FILE_READERS = {"gaugefeed.stations"}

# The only module that may read the clock: the report is handed the cycle's
# time (ADR-0002).
CLOCK_READERS = {"gaugefeed.__main__"}
CLOCK_CALLS = {"now", "utcnow", "today", "time", "monotonic"}

NETWORK_LIBRARIES = {"urllib", "http", "socket"}
NETWORK_MODULES = {"gaugefeed.fetcher"}


def module_name(path):
    parts = list(path.relative_to(PACKAGE.parent).with_suffix("").parts)
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


MODULES = {module_name(path): path for path in PACKAGE.rglob("*.py")}


def tree(name):
    return ast.parse(MODULES[name].read_text(encoding="utf-8"))


def imported_names(name):
    """Return the absolute name of every module the named module imports."""
    path = MODULES[name]
    package = name if path.name == "__init__.py" else name.rpartition(".")[0]
    names = set()
    for node in ast.walk(tree(name)):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                anchor = package.rsplit(".", node.level - 1)[0]
                base = f"{anchor}.{base}" if base else anchor
            for alias in node.names:
                submodule = f"{base}.{alias.name}"
                names.add(submodule if submodule in MODULES else base)
    return names


def declared(imported):
    """The name an import is declared by: a gaugefeed module whole, anything else by top level."""
    return imported if imported in MODULES else imported.split(".")[0]


def internal_imports(name):
    return {imported for imported in imported_names(name) if imported in MODULES} - {name}


def calls(name):
    for node in ast.walk(tree(name)):
        if isinstance(node, ast.Call):
            yield node.func


class ArchitectureTest(unittest.TestCase):
    def test_every_module_is_declared(self):
        undeclared = sorted(MODULES.keys() - ALLOWED.keys())
        self.assertEqual(undeclared, [], "declare in ALLOWED what each gaugefeed module may import")

    def test_imports_are_on_the_allow_list(self):
        for name in sorted(MODULES.keys() & ALLOWED.keys()):
            allowed, adr = ALLOWED[name]
            for imported in sorted({declared(i) for i in imported_names(name)} - allowed - {name}):
                if imported == "__future__":
                    continue
                with self.subTest(module=name, imports=imported):
                    reason = f" (see {adr})" if adr else ""
                    self.fail(f"{name} imports {imported}, which is not on its allow-list{reason}")

    def test_only_the_fetcher_imports_network_libraries(self):
        for name in sorted(MODULES.keys() - NETWORK_MODULES):
            network = sorted(i for i in imported_names(name) if i.split(".")[0] in NETWORK_LIBRARIES)
            with self.subTest(module=name):
                self.assertEqual(network, [], f"{name} talks to the network; only the fetcher "
                                              f"may (see {NETWORK_ADR})")

    def test_only_the_file_readers_open_files(self):
        for name in sorted(MODULES.keys() - FILE_READERS):
            with self.subTest(module=name):
                opens = [f for f in calls(name) if isinstance(f, ast.Name) and f.id == "open"]
                self.assertEqual(opens, [], f"{name} opens a file (see {REPORT_ADR} and {NO_STATE_ADR})")

    def test_only_main_reads_the_clock(self):
        for name in sorted(MODULES.keys() - CLOCK_READERS):
            with self.subTest(module=name):
                clock = [f.attr for f in calls(name) if isinstance(f, ast.Attribute) and f.attr in CLOCK_CALLS]
                self.assertEqual(clock, [], f"{name} reads the clock (see {REPORT_ADR})")

    def test_no_import_cycles(self):
        def find_cycle(name, trail):
            if name in trail:
                return trail[trail.index(name):] + [name]
            for imported in sorted(internal_imports(name)):
                if cycle := find_cycle(imported, trail + [name]):
                    return cycle
            return None

        for name in sorted(MODULES):
            cycle = find_cycle(name, [])
            self.assertIsNone(cycle, f"import cycle: {' -> '.join(cycle or [])}")


if __name__ == "__main__":
    unittest.main()
