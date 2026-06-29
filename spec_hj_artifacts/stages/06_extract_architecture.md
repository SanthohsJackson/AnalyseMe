# Stage: Architecture

## Data schemas
### UnitAnalysis
Represents the analysis of a code unit in a language-agnostic intermediate representation.
```json
{
  "type": "object",
  "properties": {
    "unit_id": {
      "type": "string"
    },
    "analysis_result": {
      "type": "object"
    }
  },
  "required": [
    "unit_id",
    "analysis_result"
  ]
}
```

### PipelineState
Represents the state of the pipeline execution.
```json
{
  "type": "object",
  "properties": {
    "state_id": {
      "type": "string"
    },
    "status": {
      "type": "string"
    }
  },
  "required": [
    "state_id",
    "status"
  ]
}
```

## Cross-cutting concerns
- **error_handling:** Various modules raise exceptions for error handling, such as ValueError, RuntimeError, OSError, and SystemExit, when encountering issues like invalid inputs, failed operations, or missing configurations.
- **config:** Configuration is managed using environment variables across multiple modules, such as pipeline/cache.py, pipeline/indexer.py, and cli.py. These variables configure behavior, embedding providers, models, and connection strings.
- **logging:** Logging is evidenced in pipeline/indexer.py::index_run, which logs messages during the indexing process.
- **concurrency:** Concurrency is managed using threading.BoundedSemaphore in pipeline/nodes/analyze_unit.py to control concurrency, with semaphore size adjustments ensuring concurrency control.
- **external_integrations:** __future__: used for compatibility, click: used for command-line interface parsing and handling, collections: used for data structures, datetime: used for date and time operations, enum: used for enumerations, graph: used for graph operations, hashlib: used for generating unique identifiers, json: used for JSON operations, langchain-core>=0.3: used for core language chain operations, langchain-ollama>=0.2: used for Ollama language chain operations, langchain-openai>=0.2: used for OpenAI language chain operations, langchain-postgres>=0.0.12: used for PostgreSQL language chain operations, langchain_core.documents: used for document operations, langchain_core.messages: used for message operations, langchain_core.vectorstores: used for vector store operations, langchain_ollama: used for Ollama operations, langchain_openai: used for OpenAI operations, langchain_postgres: used for PostgreSQL operations, langgraph.checkpoint.memory: used for memory checkpoint operations