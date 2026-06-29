# state_schema.py

**File:** state_schema.py  
**Language:** python

## Purpose
Define data structures and functions for analyzing and representing code units in a language-agnostic intermediate representation.

## Interfaces
### `merge_unit_analyses` (function)
```
merge_unit_analyses(existing, new)
```
**Intent:** Merge two lists of unit analyses by unit_id, ensuring the latest analysis replaces any previous one.

**Inputs:**
- existing: list[UnitAnalysis]
- new: list[UnitAnalysis]
**Outputs:**
- list[UnitAnalysis]

### `FileKind` (class)
```
class FileKind(str, Enum)
```
**Intent:** Enumerate different kinds of files in a codebase, such as source, test, config, etc.


### `FileMeta` (class)
```
class FileMeta(BaseModel)
```
**Intent:** Represent metadata about a file, including its path, language, kind, and dependencies.


### `Interface` (class)
```
class Interface(BaseModel)
```
**Intent:** Define a public surface element like a function or class, capturing its signature and intent.


### `UnitAnalysis` (class)
```
class UnitAnalysis(BaseModel)
```
**Intent:** Represent the output of a map step for an analyzable unit, detailing its purpose and interfaces.


### `UnitAnalysisResult` (class)
```
class UnitAnalysisResult(BaseModel)
```
**Intent:** Capture the intent fields of an analysis unit, separate from deterministic fields.


### `ModuleSummary` (class)
```
class ModuleSummary(BaseModel)
```
**Intent:** Summarize a module's responsibilities and public surface after an intermediate reduce step.


### `DataSchema` (class)
```
class DataSchema(BaseModel)
```
**Intent:** Define a language-neutral type description using JSON schema.


### `CrossCutting` (class)
```
class CrossCutting(BaseModel)
```
**Intent:** Capture cross-cutting concerns like error handling and logging in the system.


### `BehavioralTest` (class)
```
class BehavioralTest(BaseModel)
```
**Intent:** Define language-neutral acceptance criteria for reimplementation.


### `PipelineState` (class)
```
class PipelineState(TypedDict, total=False)
```
**Intent:** Represent the state of the pipeline, including inputs, outputs, and analysis progress.


## External dependencies
- operator
- __future__
- enum
- typing
- pydantic

## Flagged idioms
- Use of Pydantic BaseModel for data validation and serialization.
- Use of Enum for defining constant values.
