# Stage: Architecture

## Data schemas
### RunMemory
Manages cross-run memory logs.

### PipelineBuffer
Manages the state of pipeline execution, including messages and node statuses.

### BehavioralTest
Represents a behavioral test.

### CrossCutting
Represents cross-cutting concerns.

### DataSchema
Represents a data schema.

### FileKind
Represents the kind of a file.

### FileMeta
Represents metadata of a file.

### Interface
Represents an interface.

### ModuleSummary
Represents a summary of a module.

### PipelineState
Represents the state of the pipeline.

### UnitAnalysis
Represents an analysis of a code unit.

### UnitAnalysisResult
Represents the result of a unit analysis.

## Cross-cutting concerns
- **error_handling:** Various modules raise exceptions for error handling, such as when LLM calls fail, file operations fail, or database operations fail. Specific exceptions include ValueError, RuntimeError, OSError, and SystemExit.
- **config:** Configuration is managed through environment variables, which are used to configure behavior, embedding providers, models, and LLM providers. The use of Click for CLI parsing and handling is also noted.
- **logging:** Logging is implemented in the pipeline/indexer.py module, which logs messages during the indexing of runs, and in pipeline/memory.py, which writes to the memory log file.
- **concurrency:** Concurrency is managed using threading.BoundedSemaphore to control concurrency, with batch processing and try-except blocks to handle potential exceptions during LLM calls.
- **external_integrations:** __future__: used for compatibility, click: used for command-line interface parsing and handling, collections: used for data structures, datetime: used for date and time operations, enum: used for enumerations, graph: used for graph operations, hashlib: used for generating unique identifiers, json: used for JSON operations, langchain-core>=0.3: used for core language chain operations, langchain-ollama>=0.2: used for Ollama language chain operations, langchain-openai>=0.2: used for OpenAI language chain operations, langchain-postgres>=0.0.12: used for PostgreSQL language chain operations, langchain_core.documents: used for document operations, langchain_core.messages: used for message operations, langchain_core.vectorstores: used for vector store operations, langchain_ollama: used for Ollama language chain operations, langchain_openai: used for OpenAI language chain operations, langchain_postgres: used for PostgreSQL language chain operations, langgraph.checkpoint.memory: used for memory checkpoint operations