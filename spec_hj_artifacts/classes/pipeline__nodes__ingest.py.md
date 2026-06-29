# pipeline/nodes/ingest.py

**File:** pipeline/nodes/ingest.py  
**Language:** python

## Purpose
Ingest node: walk the repo, classify files, parse dependency manifests, detect entry points.

## Interfaces
### `_resolve_dependencies` (function)
```
_resolve_dependencies(files: list[FileMeta]) -> None
```
**Intent:** Resolve internal dependencies for files by matching imports to existing files in the repository.

**Inputs:**
- files: list[FileMeta] — list of file metadata objects to resolve dependencies for
**Outputs:**
- None

### `_exists` (function)
```
_exists(base: str, exts: tuple[str, ...]) -> str | None
```
**Intent:** Check if a file with the given base path and extensions exists in the repository.

**Inputs:**
- base: str — base path to check for existence
- exts: tuple[str, ...] — file extensions to consider
**Outputs:**
- str | None — resolved path if exists, otherwise None

### `_resolve_one` (function)
```
_resolve_one(imp: str, language: str, file_dir: str) -> str | None
```
**Intent:** Resolve a single import statement to a file path within the repository.

**Inputs:**
- imp: str — import statement to resolve
- language: str — programming language of the file
- file_dir: str — directory of the file
**Outputs:**
- str | None — resolved path if exists, otherwise None

### `_classify_kind` (function)
```
_classify_kind(rel_path: str, ext: str) -> FileKind
```
**Intent:** Classify the kind of a file based on its path and extension.

**Inputs:**
- rel_path: str — relative path of the file
- ext: str — file extension
**Outputs:**
- FileKind — classification of the file kind

### `_extract_imports` (function)
```
_extract_imports(source: str, language: str) -> list[str]
```
**Intent:** Extract import statements from source code based on language-specific patterns.

**Inputs:**
- source: str — source code to extract imports from
- language: str — programming language of the source code
**Outputs:**
- list[str] — list of extracted import statements

### `_parse_requirements_txt` (function)
```
_parse_requirements_txt(path: str) -> dict
```
**Intent:** Parse a Python requirements.txt file to extract dependencies.

**Inputs:**
- path: str — path to the requirements.txt file
**Outputs:**
- dict — dictionary containing type and dependencies

### `_parse_package_json` (function)
```
_parse_package_json(path: str) -> dict
```
**Intent:** Parse a Node.js package.json file to extract package information and dependencies.

**Inputs:**
- path: str — path to the package.json file
**Outputs:**
- dict — dictionary containing package information and dependencies

### `_parse_go_mod` (function)
```
_parse_go_mod(path: str) -> dict
```
**Intent:** Parse a Go go.mod file to extract module name and dependencies.

**Inputs:**
- path: str — path to the go.mod file
**Outputs:**
- dict — dictionary containing module name and dependencies

### `_parse_cargo_toml` (function)
```
_parse_cargo_toml(path: str) -> dict
```
**Intent:** Parse a Rust Cargo.toml file to extract dependencies.

**Inputs:**
- path: str — path to the Cargo.toml file
**Outputs:**
- dict — dictionary containing dependencies

### `_parse_pom_xml` (function)
```
_parse_pom_xml(path: str) -> dict
```
**Intent:** Parse a Maven pom.xml file to extract dependencies.

**Inputs:**
- path: str — path to the pom.xml file
**Outputs:**
- dict — dictionary containing dependencies

### `ingest` (function)
```
ingest() -> None
```
**Intent:** Walk the repository, classify files, parse dependency manifests, and detect entry points.

**Outputs:**
- None

## Internal dependencies
- state_schema.py

## External dependencies
- json
- os
- re
- pathlib
- xml.etree.ElementTree
- tomllib

## Flagged idioms
- Use of regular expressions for pattern matching in import extraction.
- Use of pathlib for path manipulations.

## Behavioral notes
- The function _resolve_dependencies only resolves dependencies for Python and JavaScript/TypeScript files.
