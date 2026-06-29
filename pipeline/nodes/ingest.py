"""
Ingest node: walk the repo, classify files, parse dependency manifests,
detect entry points.
"""

import json
import os
import re
import sys
from pathlib import Path

from state_schema import FileMeta, FileKind, PipelineState

# Python standard-library top-level module names, for distinguishing real
# third-party dependencies from stdlib imports (json, datetime, enum, …).
_STDLIB = set(getattr(sys, "stdlib_module_names", frozenset()))


def is_third_party(dep: str) -> bool:
    """True if `dep` looks like an external third-party package — not a stdlib
    module or a relative import. Accepts import names ('langchain_core.documents')
    and manifest specs ('langchain-core>=0.3')."""
    if not dep or dep.startswith("."):
        return False
    base = re.split(r"[<>=!~\[ .]", dep.strip())[0].replace("-", "_").lower()
    return bool(base) and base not in _STDLIB

# Same extension map as the parser
EXT_TO_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".rb": "ruby",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "c_sharp",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".lua": "lua",
    ".r": "r",
    ".R": "r",
    ".hs": "haskell",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "vendor", "dist", "build", "target", ".mypy_cache",
    ".pytest_cache", ".tox", "coverage", ".coverage",
}

# OS/editor junk files to ignore entirely (pure noise in the inventory).
SKIP_FILES = {".DS_Store", "Thumbs.db", ".llm_cache"}

# Test detection — applied to the FILENAME only (anchored), so directory
# names like "test_project" don't cause false positives.
TEST_FILENAME_PATTERNS = [
    r"^test_",        # test_foo.py
    r"_test\.",       # foo_test.go
    r"\.test\.",      # foo.test.js
    r"\.spec\.",      # foo.spec.ts
    r"^test.*\.java$",  # TestFoo.java (lowercased)
    r"test\.java$",   # FooTest.java (lowercased)
]
# Test detection — applied to whole PATH SEGMENTS (a dir named exactly
# "test"/"tests"/"spec"/"__tests__"), not substrings.
TEST_DIR_SEGMENTS = {"test", "tests", "spec", "specs", "__tests__", "testing"}

CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env", ".conf"}
BUILD_FILES = {
    "makefile", "dockerfile", "jenkinsfile", "rakefile",
    "cmakelists.txt", ".travis.yml", ".github",
}
DOC_EXTS = {".md", ".rst", ".txt", ".adoc", ".org"}

ENTRY_POINT_NAMES = {
    "main.py", "app.py", "server.py", "cli.py", "__main__.py",
    "index.js", "index.ts", "main.js", "main.ts",
    "main.go", "main.rs", "Main.java",
}

IMPORT_PATTERNS: dict[str, list[str]] = {
    "python": [r"^\s*import\s+([\w.]+)", r"^\s*from\s+([\w.]+)\s+import"],
    "javascript": [r"""(?:import|require)\s*\(?['"]([^'"]+)['"]\)?"""],
    "typescript": [r"""(?:import|require)\s*\(?['"]([^'"]+)['"]\)?"""],
    "go": [r'"([^"]+)"'],
    "rust": [r"^use\s+([\w:]+)"],
    "java": [r"^import\s+([\w.]+);"],
    "ruby": [r"""^require(?:_relative)?\s+['"]([^'"]+)['"]"""],
    "cpp": [r'#include\s+[<"]([^>"]+)[>"]'],
    "c": [r'#include\s+[<"]([^>"]+)[>"]'],
    "c_sharp": [r"^using\s+([\w.]+);"],
}


# Candidate file extensions when resolving an import to a repo file, per language.
_RESOLVE_EXTS = {
    "python": (".py",),
    "javascript": (".js", ".jsx", ".ts", ".tsx"),
    "typescript": (".ts", ".tsx", ".js", ".jsx"),
}


def _resolve_dependencies(files: list[FileMeta]) -> None:
    """Populate FileMeta.depends_on by resolving raw imports to repo-relative
    paths of other files in *this* repo (internal dependencies).

    Deterministic and conservative: a dependency is recorded only when an import
    resolves to a file that actually exists in the repo. Third-party/stdlib
    imports that don't resolve are left out. Covers Python and JS/TS (relative
    and root-package imports); other languages get no resolution (better empty
    than wrong — see the pipeline's "deterministic facts only" design).
    """
    all_paths = {fm.path.replace(os.sep, "/") for fm in files}

    def _exists(base: str, exts: tuple[str, ...]) -> str | None:
        for e in exts:
            if (cand := base + e) in all_paths:
                return cand
        # package/index style: foo/__init__.py (py) or foo/index.ts (js/ts)
        for e in exts:
            idx = "__init__" if e == ".py" else "index"
            if (cand := f"{base}/{idx}{e}") in all_paths:
                return cand
        return None

    def _resolve_one(imp: str, language: str, file_dir: str) -> str | None:
        exts = _RESOLVE_EXTS.get(language)
        if not exts:
            return None
        if language in ("javascript", "typescript"):
            if imp.startswith("."):  # only relative specifiers can be internal
                base = os.path.normpath(os.path.join(file_dir, imp)).replace(os.sep, "/")
                return _exists(base, exts)
            return None
        # python
        if imp.startswith("."):  # relative import: leading dots = levels up
            dots = len(imp) - len(imp.lstrip("."))
            rest = imp[dots:]
            up = file_dir
            for _ in range(dots - 1):
                up = os.path.dirname(up)
            base = os.path.normpath(os.path.join(up, rest.replace(".", "/"))).replace(os.sep, "/") if rest else up
            return _exists(base, exts)
        # absolute import: try the full dotted path, then drop trailing segments
        parts = imp.split(".")
        while parts:
            if (hit := _exists("/".join(parts), exts)):
                return hit
            parts = parts[:-1]
        return None

    for fm in files:
        if not fm.language or not fm.imports:
            continue
        self_posix = fm.path.replace(os.sep, "/")
        file_dir = os.path.dirname(self_posix)
        resolved = []
        for imp in fm.imports:
            target = _resolve_one(imp, fm.language, file_dir)
            if target and target != self_posix:
                resolved.append(target)
        fm.depends_on = sorted(dict.fromkeys(resolved))


def _classify_kind(rel_path: str, ext: str) -> FileKind:
    filename = Path(rel_path).name.lower()
    segments = {seg.lower() for seg in Path(rel_path).parts[:-1]}  # dirs only

    is_test = (
        any(re.search(p, filename) for p in TEST_FILENAME_PATTERNS)
        or bool(segments & TEST_DIR_SEGMENTS)
    )
    if is_test:
        return FileKind.TEST
    if ext in DOC_EXTS:
        return FileKind.DOC
    if filename in BUILD_FILES or ext in {".gradle", ".mk"}:
        return FileKind.BUILD
    if filename in {
        "package.json", "go.mod", "cargo.toml", "pom.xml",
        "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
        "gemfile", "composer.json",
    }:
        return FileKind.BUILD
    if ext in CONFIG_EXTS:
        return FileKind.CONFIG
    if ext in EXT_TO_LANG:
        return FileKind.SOURCE
    return FileKind.OTHER


def _extract_imports(source: str, language: str) -> list[str]:
    patterns = IMPORT_PATTERNS.get(language, [])
    imports = []
    for pattern in patterns:
        for m in re.finditer(pattern, source, re.MULTILINE):
            imports.append(m.group(1))
    return list(set(imports))


def _parse_requirements_txt(path: str) -> dict:
    deps = []
    try:
        with open(path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    deps.append(line)
    except OSError:
        pass
    return {"type": "python", "dependencies": deps}


def _parse_package_json(path: str) -> dict:
    try:
        with open(path, "r", errors="replace") as f:
            data = json.load(f)
        return {
            "type": "node",
            "name": data.get("name", ""),
            "version": data.get("version", ""),
            "dependencies": list(data.get("dependencies", {}).keys()),
            "devDependencies": list(data.get("devDependencies", {}).keys()),
        }
    except Exception:
        return {"type": "node", "dependencies": []}


def _parse_go_mod(path: str) -> dict:
    deps = []
    module_name = ""
    try:
        with open(path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line.startswith("module "):
                    module_name = line.split()[1]
                elif line and not line.startswith("//") and not line.startswith("go "):
                    parts = line.split()
                    if parts:
                        deps.append(parts[0])
    except OSError:
        pass
    return {"type": "go", "module": module_name, "dependencies": deps}


def _parse_cargo_toml(path: str) -> dict:
    deps = []
    try:
        import tomllib  # Python 3.11+
        with open(path, "rb") as f:
            data = tomllib.load(f)
        deps = list(data.get("dependencies", {}).keys())
    except Exception:
        # Fallback: regex
        try:
            with open(path, "r", errors="replace") as f:
                content = f.read()
            in_deps = False
            for line in content.splitlines():
                if line.strip() == "[dependencies]":
                    in_deps = True
                    continue
                if in_deps and line.strip().startswith("["):
                    in_deps = False
                if in_deps and "=" in line:
                    deps.append(line.split("=")[0].strip())
        except OSError:
            pass
    return {"type": "rust", "dependencies": deps}


def _parse_pom_xml(path: str) -> dict:
    deps = []
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()
        ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
        prefix = f"{{{ns}}}" if ns else ""
        for dep in root.iter(f"{prefix}dependency"):
            artifact = dep.find(f"{prefix}artifactId")
            if artifact is not None and artifact.text:
                deps.append(artifact.text)
    except Exception:
        pass
    return {"type": "java_maven", "dependencies": deps}


MANIFEST_PARSERS = {
    "requirements.txt": _parse_requirements_txt,
    "package.json": _parse_package_json,
    "go.mod": _parse_go_mod,
    "cargo.toml": _parse_cargo_toml,
    "pom.xml": _parse_pom_xml,
}


def ingest(state: PipelineState) -> dict:
    repo_path = state["repo_path"]
    files: list[FileMeta] = []
    languages_detected: set[str] = set()
    entry_points: list[str] = []
    dependency_manifest: dict = {}

    for dirpath, dirnames, filenames in os.walk(repo_path):
        # Prune skipped directories in-place. Also drop this pipeline's own
        # generated output (e.g. <spec>_artifacts/) so we never analyse our specs.
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
            and not d.endswith(".egg-info")
            and not d.endswith("_artifacts")
        ]

        for filename in filenames:
            # Skip OS/editor junk that only adds noise to the inventory.
            if filename in SKIP_FILES:
                continue
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, repo_path)
            ext = Path(filename).suffix.lower()
            language = EXT_TO_LANG.get(ext)
            kind = _classify_kind(rel_path, ext)

            # Count LOC
            loc = 0
            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    loc = sum(1 for line in f if line.strip())
            except OSError:
                pass

            # Extract imports
            imports: list[str] = []
            if language and kind == FileKind.SOURCE:
                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                        source = f.read()
                    imports = _extract_imports(source, language)
                except OSError:
                    pass

            if language:
                languages_detected.add(language)

            file_meta = FileMeta(
                path=rel_path,
                language=language,
                kind=kind,
                loc=loc,
                imports=imports,
            )
            files.append(file_meta)

            # Detect entry points
            if filename in ENTRY_POINT_NAMES:
                entry_points.append(rel_path)

            # Parse dependency manifests
            lower_name = filename.lower()
            if lower_name in MANIFEST_PARSERS:
                parser_fn = MANIFEST_PARSERS[lower_name]
                try:
                    dependency_manifest[rel_path] = parser_fn(full_path)
                except Exception:
                    pass

    # Resolve internal dependencies deterministically (imports -> repo files).
    _resolve_dependencies(files)

    return {
        "files": files,
        "languages_detected": sorted(languages_detected),
        "entry_points": entry_points,
        "dependency_manifest": dependency_manifest,
    }
