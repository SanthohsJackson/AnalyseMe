# pipeline/parsers/tree_sitter_parser.py

**File:** pipeline/parsers/tree_sitter_parser.py  
**Language:** python

## Purpose
Extracts code structure using Tree-sitter for various programming languages.

## Interfaces
### `_get_lang_from_path` (function)
```
_get_lang_from_path(path: str) -> str | None
```
**Intent:** Determine the programming language from a file extension.

**Inputs:**
- path: str — the file path to determine the language from
**Outputs:**
- str | None — the language name or None if not found

### `_get_ts_parser` (function)
```
_get_ts_parser(language: str)
```
**Intent:** Retrieve a Tree-sitter parser for a given language, preferring maintained packages.

**Inputs:**
- language: str — the language to get a parser for
**Outputs:**
- Parser | None — a Tree-sitter parser or None if unavailable

### `_extract_go_imports` (function)
```
_extract_go_imports(source: str) -> list[str]
```
**Intent:** Extract Go import paths from source code, handling both grouped and single-line imports.

**Inputs:**
- source: str — the source code to extract imports from
**Outputs:**
- list[str] — a list of Go import paths

### `_extract_imports_regex` (function)
```
_extract_imports_regex(source: str, language: str) -> list[str]
```
**Intent:** Extract import paths using regex patterns specific to the language.

**Inputs:**
- source: str — the source code to extract imports from
- language: str — the language of the source code
**Outputs:**
- list[str] — a list of import paths

### `_count_loc` (function)
```
_count_loc(source: str) -> int
```
**Intent:** Count the number of non-blank lines in the source code.

**Inputs:**
- source: str — the source code to count lines of
**Outputs:**
- int — the number of non-blank lines

### `_structure` (function)
```
_structure(functions: list, classes: list, imports: list, loc: int) -> dict
```
**Intent:** Build a structured representation of the code's functions, classes, imports, and LOC.

**Inputs:**
- functions: list — list of function names
- classes: list — list of class names
- imports: list — list of import statements
- loc: int — lines of code count
**Outputs:**
- dict — structured representation of the code

### `_empty_structure` (function)
```
_empty_structure(source: str) -> dict
```
**Intent:** Create an empty structure with only the LOC count.

**Inputs:**
- source: str — the source code to analyze
**Outputs:**
- dict — empty structure with LOC count

### `_first_name` (function)
```
_first_name(node, source_bytes: bytes) -> str | None
```
**Intent:** Extract the name of a declaration from an AST node.

**Inputs:**
- node — the AST node to extract the name from
- source_bytes: bytes — the source code in bytes
**Outputs:**
- str | None — the name of the declaration or None

### `_traverse_for_names` (function)
```
_traverse_for_names(node, source_bytes: bytes, functions: list, classes: list)
```
**Intent:** Recursively traverse the AST to collect function and class names.

**Inputs:**
- node — the AST node to traverse
- source_bytes: bytes — the source code in bytes
- functions: list — list to collect function names
- classes: list — list to collect class names

### `_collect_class_spans` (function)
```
_collect_class_spans(node, source_bytes: bytes, out: list, inside_class: bool = False) -> None
```
**Intent:** Collect byte and line spans of top-level classes in the source code.

**Inputs:**
- node — the AST node to traverse
- source_bytes: bytes — the source code in bytes
- out: list — list to collect class spans
- inside_class: bool — flag indicating if inside a class

### `extract_class_spans` (function)
```
extract_class_spans(path: str) -> list[dict]
```
**Intent:** Return byte and line spans of top-level classes in a file.

**Inputs:**
- path: str — the file path to extract class spans from
**Outputs:**
- list[dict] — list of class spans with byte and line information

### `parse_file` (function)
```
parse_file(path: str)
```
**Intent:** Parse a file to extract its structure using Tree-sitter.

**Inputs:**
- path: str — the file path to parse

## External dependencies
- logging
- re
- pathlib
- tree_sitter_language_pack
- tree_sitter_languages

## Flagged idioms
- Use of Tree-sitter for language-agnostic AST traversal and analysis.

## Behavioral notes
- Graceful fallback to regex-based import extraction when Tree-sitter grammar is unsupported.
