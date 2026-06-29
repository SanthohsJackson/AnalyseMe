# Stage: Architecture

## Data schemas
### UnitAnalysis
Represents the analysis of a code unit in a language-agnostic intermediate representation.

### UnitAnalysisResult
Holds the results of a unit analysis.

### PipelineState
Represents the state of the pipeline execution.

### ModuleSummary
Summarizes a module's characteristics.

### FileMeta
Metadata for a file in the repository.

### FileKind
Represents the kind of file in the repository.

### Interface
Represents an interface in the codebase.

### DataSchema
Represents a data schema in the codebase.

### CrossCutting
Represents cross-cutting concerns in the codebase.

### BehavioralTest
Represents a behavioral test in the codebase.

## Cross-cutting concerns
- **error_handling:** The system raises various exceptions for error handling, such as Exception, ValueError, RuntimeError, OSError, and SystemExit, in different modules when operations fail (e.g., LLM call failures, repository resolution issues, database operation failures).
- **config:** Configuration is managed using environment variables across multiple modules, such as pipeline/cache.py, pipeline/indexer.py, pipeline/model_catalog.py, cli.py, pipeline/vectordb.py, and pipeline/llm.py. These variables configure behavior, embedding providers, models, and connection strings.
- **logging:** Logging is evidenced in pipeline/indexer.py::index_run, which logs messages during the indexing process.
- **concurrency:** Concurrency is managed using threading.BoundedSemaphore in pipeline/nodes/analyze_unit.py to control concurrency, with semaphore size adjustments ensuring concurrency control. Batch processing and try-except blocks are used in pipeline/nodes/generate_tests.py.
- **external_integrations:** __future__: used for compatibility, click: used for command-line interface parsing and handling, collections: used for data structures, datetime: used for date and time operations, enum: used for enumerations, graph: used for graph operations, hashlib: used for generating unique identifiers, json: used for JSON operations, langchain-core>=0.3: used for core language chain operations, langchain-ollama>=0.2: used for Ollama language chain operations, langchain-openai>=0.2: used for OpenAI language chain operations, langchain-postgres>=0.0.12: used for PostgreSQL language chain operations, langchain_core.documents: used for document operations, langchain_core.messages: used for message operations, langchain_core.vectorstores: used for vector store operations, langchain_ollama: used for Ollama operations, langchain_openai: used for OpenAI operations, langchain_postgres: used for PostgreSQL operations, langgraph.checkpoint.memory: used for memory checkpoint operations