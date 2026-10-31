"""Checks the import rules between gaugefeed's modules."""

import ast
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "gaugefeed"

NETWORK_ADR = "docs/adr/0001-only-the-fetcher-talks-to-the-network.md"
REPORT_ADR = "docs/adr/0002-the-report-is-built-from-readings-alone.md"

# Every module in the package, the gaugefeed modules it may import, and the
# decision record that drew that list (None where nobody decided it).
ALLOWED = {
    "gaugefeed": (set(), None),
    "gaugefeed.__main__": ({"gaugefeed.stations", "gaugefeed.fetcher", "gaugefeed.report"}, None),
    "gaugefeed.stations": (set(), None),
    "gaugefeed.fetcher": (set(), None),
    "gaugefeed.report": (set(), REPORT_ADR),
}

NETWORK_LIBRARIES = {"urllib", "http", "socket"}
NETWORK_MODULES = {"gaugefeed.fetcher"}


def module_name(path):
    parts = list(path.relative_to(PACKAGE.parent).with_suffix("").parts)
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


MODULES = {module_name(path): path for path in PACKAGE.rglob("*.py")}


def imported_names(name):
    """Return the absolute name of every module the named module imports."""
    path = MODULES[name]
    package = name if path.name == "__init__.py" else name.rpartition(".")[0]
    names = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
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


def internal_imports(name):
    return {imported for imported in imported_names(name) if imported in MODULES} - {name}


class ArchitectureTest(unittest.TestCase):
    def test_every_module_is_declared(self):
        undeclared = sorted(MODULES.keys() - ALLOWED.keys())
        self.assertEqual(undeclared, [], "declare in ALLOWED which gaugefeed modules each may import")

    def test_internal_imports_are_on_the_allow_list(self):
        for name in sorted(MODULES.keys() & ALLOWED.keys()):
            allowed, adr = ALLOWED[name]
            for imported in sorted(internal_imports(name) - allowed):
                with self.subTest(module=name, imports=imported):
                    reason = f" (see {adr})" if adr else ""
                    self.fail(f"{name} imports {imported}, which is not on its allow-list{reason}")

    def test_only_the_fetcher_imports_network_libraries(self):
        for name in sorted(MODULES.keys() - NETWORK_MODULES):
            network = sorted(i for i in imported_names(name) if i.split(".")[0] in NETWORK_LIBRARIES)
            with self.subTest(module=name):
                self.assertEqual(network, [], f"{name} talks to the network; only the fetcher "
                                              f"may (see {NETWORK_ADR})")

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
