# pipeline/nodes/route_units.py

**File:** pipeline/nodes/route_units.py  
**Language:** python

## Purpose
Create unit descriptors for fan-out analysis in a pipeline.

## Interfaces
### `_file_units` (function)
```
_file_units(file_meta, repo_path: str, max_parallelism: int) -> list[dict]
```
**Intent:** Generate unit descriptors for a source file, splitting large files into class-based units if possible.

**Inputs:**
- file_meta: object — metadata of the file
- repo_path: str — path to the repository
- max_parallelism: int — maximum parallelism allowed
**Outputs:**
- list[dict] — list of unit descriptors

### `route_units` (function)
```
route_units(state: PipelineState) -> dict
```
**Intent:** Determine eligible source files and generate unit descriptors for analysis, prioritizing smaller files for faster feedback.

**Inputs:**
- state: PipelineState — current state of the pipeline
**Outputs:**
- dict — dictionary containing units to analyze
**Side effects:**
- prints the number of units queued

## Internal dependencies
- pipeline/parsers/tree_sitter_parser.py
- state_schema.py

## External dependencies
- os

## Flagged idioms
- Use of list comprehensions for filtering and sorting files based on conditions.

## Behavioral notes
- The function _file_units handles both small and large files differently, attempting to split large files into class-based units.
- route_units prioritizes smaller files for early feedback and can limit the number of files processed based on max_files.
