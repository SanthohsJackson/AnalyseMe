"""
Tree-sitter based deterministic code structure extractor.
Extracts function/method names, class names, imports, and LOC counts.
Falls back gracefully when the language grammar is not supported.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Map file extensions to tree-sitter language names
EXT_TO_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
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
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".scss": "css",
}

# Regex fallbacks for import extraction per language
IMPORT_PATTERNS = {
    "python": [
        r"^\s*import\s+([\w.]+)",
        r"^\s*from\s+([\w.]+)\s+import",
    ],
    "javascript": [
        r"""(?:import|require)\s*\(?['"]([^'"]+)['"]\)?""",
    ],
    "typescript": [
        r"""(?:import|require)\s*\(?['"]([^'"]+)['"]\)?""",
    ],
    # Go is handled specially by _extract_go_imports (a bare quoted-string regex
    # would match every string literal in the file, not just imports).
    "rust": [
        r"^use\s+([\w:]+)",
    ],
    "java": [
        r"^import\s+([\w.]+);",
    ],
    "ruby": [
        r"""^require\s+['"]([^'"]+)['"]""",
        r"""^require_relative\s+['"]([^'"]+)['"]""",
    ],
    "cpp": [
        r'#include\s+[<"]([^>"]+)[>"]',
    ],
    "c": [
        r'#include\s+[<"]([^>"]+)[>"]',
    ],
    "c_sharp": [
        r"^using\s+([\w.]+);",
    ],
}


def _get_lang_from_path(path: str) -> str | None:
    ext = Path(path).suffix.lower()
    return EXT_TO_LANG.get(ext)


def _get_ts_parser(language: str):
    """Return a tree-sitter Parser for the language, or None.

    Prefers the maintained `tree-sitter-language-pack` (compatible with current
    tree-sitter core); falls back to the legacy `tree_sitter_languages`.
    """
    try:
        from tree_sitter_language_pack import get_parser  # type: ignore
        return get_parser(language)
    except Exception:
        pass
    try:
        from tree_sitter_languages import get_parser  # type: ignore
        return get_parser(language)
    except Exception:
        return None


def _extract_go_imports(source: str) -> list[str]:
    """Extract Go import paths, scoped to import statements only.

    Handles both the grouped form `import ( "a"; "b" )` and single-line
    `import [alias] "pkg"`, so string literals elsewhere in the file are not
    mistaken for imports.
    """
    imports = []
    # Grouped: import ( ... ) — Go import blocks contain no ')', so [^)] is safe.
    for block in re.finditer(r"import\s*\(([^)]*)\)", source, re.DOTALL):
        for m in re.finditer(r'"([^"]+)"', block.group(1)):
            imports.append(m.group(1))
    # Single-line: import "pkg", import alias "pkg", import . "pkg", import _ "pkg"
    for m in re.finditer(r'^\s*import\s+(?:[\w.]+\s+|\.\s+|_\s+)?"([^"]+)"', source, re.MULTILINE):
        imports.append(m.group(1))
    return list(dict.fromkeys(imports))


def _extract_imports_regex(source: str, language: str) -> list[str]:
    if language == "go":
        return _extract_go_imports(source)
    patterns = IMPORT_PATTERNS.get(language, [])
    imports = []
    for pattern in patterns:
        for match in re.finditer(pattern, source, re.MULTILINE):
            imports.append(match.group(1))
    return list(dict.fromkeys(imports))


def _count_loc(source: str) -> int:
    """Count non-blank lines."""
    return len([line for line in source.splitlines() if line.strip()])


def _structure(functions: list, classes: list, imports: list, loc: int) -> dict:
    """Build the canonical structure dict — the single definition of the output schema."""
    return {
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "loc": loc,
    }


def _empty_structure(source: str) -> dict:
    return _structure([], [], [], _count_loc(source))


# Node types that define a function/method, across languages
_FUNC_NODE_TYPES = {
    "function_definition", "async_function_def",          # python
    "function_declaration", "generator_function_declaration",  # js/ts/go
    "method_definition",                                   # js/ts
    "method_declaration",                                  # java/go/c#
    "function_item",                                       # rust
    "constructor_declaration",                             # java/c#
}
# Node types that define a class/type, across languages. This is the canonical
# "class-like" set, used both for name extraction (_traverse_for_names) and for
# splitting large files into per-class units (_collect_class_spans).
_CLASS_NODE_TYPES = {
    "class_definition",                                    # python
    "class_declaration", "class",                          # java/js/ts/c#
    "interface_declaration", "enum_declaration", "record_declaration",  # java/ts
    "struct_item", "enum_item", "trait_item", "impl_item", # rust
}
# Child node types that carry the declared name
_NAME_CHILD_TYPES = ("identifier", "field_identifier", "property_identifier",
                     "type_identifier", "name", "constant")


def _first_name(node, source_bytes: bytes) -> str | None:
    """Robustly get a declaration's name.

    Prefer tree-sitter's named fields ('name', then 'type' for Rust impls) so we
    don't accidentally grab a method's return type; fall back to the first
    identifier-like child.
    """
    for field in ("name", "type"):
        try:
            n = node.child_by_field_name(field)
        except Exception:
            n = None
        if n is not None:
            return source_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="replace")
    for child in node.children:
        if child.type in _NAME_CHILD_TYPES:
            return source_bytes[child.start_byte:child.end_byte].decode("utf-8", errors="replace")
    return None


def _traverse_for_names(node, source_bytes: bytes, functions: list, classes: list):
    """Recursively walk the AST collecting function/class names (language-agnostic)."""
    if node.type in _FUNC_NODE_TYPES:
        name = _first_name(node, source_bytes)
        if name:
            functions.append(name)
    elif node.type in _CLASS_NODE_TYPES:
        name = _first_name(node, source_bytes)
        if name:
            classes.append(name)

    for child in node.children:
        _traverse_for_names(child, source_bytes, functions, classes)


def _collect_class_spans(node, source_bytes: bytes, out: list, inside_class: bool = False) -> None:
    is_class = node.type in _CLASS_NODE_TYPES
    if is_class and not inside_class:
        name = _first_name(node, source_bytes) or "<anonymous>"
        out.append({
            "name": name,
            "start_byte": node.start_byte,
            "end_byte": node.end_byte,
            "start_line": node.start_point[0] + 1,
            "end_line": node.end_point[0] + 1,
        })
    for child in node.children:
        _collect_class_spans(child, source_bytes, out, inside_class or is_class)


def extract_class_spans(path: str) -> list[dict]:
    """Return byte/line spans of top-level classes in a file (empty if none/unsupported).

    Used to split large files into per-class analysis units so their content is
    not truncated.
    """
    try:
        with open(path, "rb") as f:
            source_bytes = f.read()
    except OSError:
        return []

    language = _get_lang_from_path(path)
    if language is None:
        return []
    try:
        parser = _get_ts_parser(language)
        if parser is None:
            return []
        tree = parser.parse(source_bytes)
        spans: list[dict] = []
        _collect_class_spans(tree.root_node, source_bytes, spans)
        # Sort by position, drop zero-length
        return [s for s in sorted(spans, key=lambda s: s["start_byte"]) if s["end_byte"] > s["start_byte"]]
    except Exception as exc:
        logger.debug("class-span extraction failed for %s: %s", path, exc)
        return []


def _walk_classes(node):
    if node.type in _CLASS_NODE_TYPES:
        yield node
    for child in node.children:
        yield from _walk_classes(child)


def extract_class_fields(path: str) -> dict:
    """Return {class_name: [{"name", "type"}]} of annotated data fields.

    Captures class-level annotated assignments (``name: type [= ...]``) — the
    fields of Pydantic models, dataclasses, and TypedDicts. Python-only for now;
    other languages return {} (graceful). Deterministic ground truth for the
    data model, so schemas aren't guessed by the LLM.
    """
    try:
        with open(path, "rb") as f:
            source_bytes = f.read()
    except OSError:
        return {}

    if _get_lang_from_path(path) != "python":
        return {}
    try:
        parser = _get_ts_parser("python")
        if parser is None:
            return {}
        tree = parser.parse(source_bytes)
    except Exception:
        return {}

    def _text(node) -> str:
        return source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

    out: dict[str, list] = {}
    for cls in _walk_classes(tree.root_node):
        name = _first_name(cls, source_bytes)
        body = cls.child_by_field_name("body")
        if not name or body is None:
            continue
        fields = []
        for stmt in body.children:
            if stmt.type != "expression_statement":
                continue
            for ch in stmt.children:
                if ch.type != "assignment":
                    continue
                ty = ch.child_by_field_name("type")
                left = ch.child_by_field_name("left")
                if ty is not None and left is not None and left.type == "identifier":
                    fields.append({"name": _text(left), "type": _text(ty)})
        if fields:
            out[name] = fields
    return out


def parse_file(path: str) -> dict:
    """
    Parse a source file with tree-sitter and return extracted structure.

    Returns:
        {
            "functions": [str, ...],
            "classes": [str, ...],
            "imports": [str, ...],
            "loc": int,
        }
    Falls back gracefully if language not supported.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
    except OSError:
        return _empty_structure("")

    language = _get_lang_from_path(path)
    loc = _count_loc(source)

    if language is None:
        return _structure([], [], [], loc)

    # Try tree-sitter extraction
    try:
        parser = _get_ts_parser(language)
        if parser is None:
            raise RuntimeError("no tree-sitter parser")
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)

        functions: list[str] = []
        classes: list[str] = []
        _traverse_for_names(tree.root_node, source_bytes, functions, classes)

        # Keep duplicate names (overloads, same-named methods across classes) so the
        # inventory is faithful; AST traversal order keeps the output deterministic.
        imports = _extract_imports_regex(source, language)
        return _structure(functions, classes, imports, loc)
    except Exception as exc:
        # tree-sitter not available or grammar missing — fall back to regex imports.
        logger.debug("tree-sitter parse failed for %s (%s); using regex fallback", path, exc)
        imports = _extract_imports_regex(source, language)
        return _structure([], [], imports, loc)
