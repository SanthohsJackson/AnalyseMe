# Stage: Architecture

## Data schemas
### RunMemory
Manages cross-run memory logs.

### PipelineBuffer
Manages the state of pipeline execution, including messages and node statuses.

### BehavioralTest
Represents a behavioral test in the pipeline.

### CrossCutting
Represents cross-cutting concerns in the pipeline.

### DataSchema
Represents data schemas for analyzing and representing code units in a language-agnostic intermediate representation.

### FileKind
Represents the kind of a file in the pipeline.

### FileMeta
Represents metadata of a file in the pipeline.

### Interface
Represents an interface in the pipeline.

### ModuleSummary
Represents a summary of a module in the pipeline.

### PipelineState
Represents the state of the pipeline.

### UnitAnalysis
Represents the analysis of a code unit.

### UnitAnalysisResult
Represents the result of a unit analysis.

## Cross-cutting concerns
- **config:** The 'pipeline' module configures model providers and manages pipeline execution configuration through the CLI.
- **external_integrations:** Tree-sitter: Used for extracting code structure in the 'pipeline/parsers' module., Large language models: Interacted with through helper functions in the 'pipeline' module.