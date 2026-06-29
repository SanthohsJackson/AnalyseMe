# Stage: Architecture Diagram

#### Module Dependencies

```mermaid
graph LR
    m__["(root)"]
    m_cli["cli"]
    m_pipeline["pipeline"]
    m_pipeline_nodes["pipeline/nodes"]
    m_pipeline_parsers["pipeline/parsers"]
    m_pipeline_prompts["pipeline/prompts"]
    m__ --> m_cli
    m__ --> m_pipeline
    m__ --> m_pipeline_nodes
    m_cli --> m__
    m_cli --> m_pipeline
    m_cli --> m_pipeline_prompts
    m_pipeline_nodes --> m__
    m_pipeline_nodes --> m_pipeline
    m_pipeline_nodes --> m_pipeline_parsers
    m_pipeline_nodes --> m_pipeline_prompts
    style m__ fill:#cce5ff,stroke:#004085,stroke-width:2px
    style m_cli fill:#cce5ff,stroke:#004085,stroke-width:2px
```

_Entry-point modules are highlighted. Edges are resolved imports between modules._

#### External Integrations

```mermaid
graph LR
    sys_system["AnalyseMe"]
    m___future__(["__future__"])
    sys_system -->|"used for compatibility"| m___future__
    m_click(["click"])
    sys_system -->|"used for command-line interface parsing …"| m_click
    m_collections(["collections"])
    sys_system -->|"used for data structures"| m_collections
    m_datetime(["datetime"])
    sys_system -->|"used for date and time operations"| m_datetime
    m_enum(["enum"])
    sys_system -->|"used for enumerations"| m_enum
    m_graph(["graph"])
    sys_system -->|"used for graph operations"| m_graph
    m_hashlib(["hashlib"])
    sys_system -->|"used for generating unique identifiers"| m_hashlib
    m_json(["json"])
    sys_system -->|"used for JSON operations"| m_json
    m_langchain_core__0_3(["langchain-core>=0.3"])
    sys_system -->|"used for core language chain operations"| m_langchain_core__0_3
    m_langchain_ollama__0_2(["langchain-ollama>=0.2"])
    sys_system -->|"used for Ollama language chain operation…"| m_langchain_ollama__0_2
    m_langchain_openai__0_2(["langchain-openai>=0.2"])
    sys_system -->|"used for OpenAI language chain operation…"| m_langchain_openai__0_2
    m_langchain_postgres__0_0_12(["langchain-postgres>=0.0.12"])
    sys_system -->|"used for PostgreSQL language chain opera…"| m_langchain_postgres__0_0_12
    m_langchain_core_documents(["langchain_core.documents"])
    sys_system -->|"used for document operations"| m_langchain_core_documents
    m_langchain_core_messages(["langchain_core.messages"])
    sys_system -->|"used for message operations"| m_langchain_core_messages
    m_langchain_core_vectorstores(["langchain_core.vectorstores"])
    sys_system -->|"used for vector store operations"| m_langchain_core_vectorstores
    m_langchain_ollama(["langchain_ollama"])
    sys_system -->|"used for Ollama language chain operation…"| m_langchain_ollama
    m_langchain_openai(["langchain_openai"])
    sys_system -->|"used for OpenAI language chain operation…"| m_langchain_openai
    m_langchain_postgres(["langchain_postgres"])
    sys_system -->|"used for PostgreSQL language chain opera…"| m_langchain_postgres
    m_langgraph_checkpoint_memory(["langgraph.checkpoint.memory"])
    sys_system -->|"used for memory checkpoint operations"| m_langgraph_checkpoint_memory
    style m_langchain_core__0_3 fill:#fff3cd,stroke:#856404
    style m_langchain_postgres fill:#fff3cd,stroke:#856404
    style m_langchain_ollama__0_2 fill:#fff3cd,stroke:#856404
    style m_enum fill:#fff3cd,stroke:#856404
    style m_json fill:#fff3cd,stroke:#856404
    style m_langchain_core_messages fill:#fff3cd,stroke:#856404
    style m_langchain_openai fill:#fff3cd,stroke:#856404
    style m_hashlib fill:#fff3cd,stroke:#856404
    style m_langchain_openai__0_2 fill:#fff3cd,stroke:#856404
    style m_datetime fill:#fff3cd,stroke:#856404
    style m_graph fill:#fff3cd,stroke:#856404
    style m_click fill:#fff3cd,stroke:#856404
    style m_collections fill:#fff3cd,stroke:#856404
    style m_langchain_core_documents fill:#fff3cd,stroke:#856404
    style m___future__ fill:#fff3cd,stroke:#856404
    style m_langchain_ollama fill:#fff3cd,stroke:#856404
    style m_langgraph_checkpoint_memory fill:#fff3cd,stroke:#856404
    style m_langchain_core_vectorstores fill:#fff3cd,stroke:#856404
    style m_langchain_postgres__0_0_12 fill:#fff3cd,stroke:#856404
```

_External services the system integrates with (rounded nodes)._

#### Data Model

```mermaid
classDiagram
    class RunMemory
    class PipelineBuffer
    class BehavioralTest
    class CrossCutting
    class DataSchema
    class FileKind
    class FileMeta
    class Interface
    class ModuleSummary
    class PipelineState
    class UnitAnalysis
    class UnitAnalysisResult
```

_Data entities from the extracted schemas; arrows show references between them._