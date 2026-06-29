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
    m_Tree_sitter(["Tree-sitter"])
    sys_system -->|"Used for extracting code structure in th…"| m_Tree_sitter
    m_Large_language_models(["Large language models"])
    sys_system -->|"Interacted with through helper functions…"| m_Large_language_models
    style m_Tree_sitter fill:#fff3cd,stroke:#856404
    style m_Large_language_models fill:#fff3cd,stroke:#856404
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