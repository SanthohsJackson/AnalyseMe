# Reimplementation Specification Document

## 1. Inventory

### File Tree Summary
- **Languages Detected**: Bash, Python
- **Total Files**: 414

### Languages
- **Bash**: 1 file
  - `run.sh`
- **Python**: 39 files
  - `cli.py`
  - `cli/__init__.py`
  - `cli/main.py`
  - `main.py`
  - `pipeline/__init__.py`
  - `pipeline/cache.py`
  - `pipeline/llm.py`
  - `pipeline/nodes/__init__.py`
  - `pipeline/nodes/extract_architecture.py`
  - `pipeline/nodes/generate_tests.py`
  - ... and 29 more

### Dependencies
- **Dependency Manifests**: `requirements.txt`
  - `langgraph>=0.2`
  - `langchain-core>=0.3`
  - `langchain-ollama>=0.2`
  - `langchain-openai>=0.2`
  - `langsmith>=0.1`
  - `tree-sitter==0.21.3`
  - `tree-sitter-languages==1.10.2`
  - `pydantic>=2.0`
  - `click>=8.0`
  - `rich>=13.0`
  - ... and 6 more

### Entry Points
- `cli.py`
- `main.py`
- `cli/main.py`

## 2. Architecture

### Architecture Diagram

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


### Components
- **Main Module**: Entry point for executing the CLI application.
- **CLI Module**: Provides a command-line interface for configuring and managing the pipeline.
- **Pipeline Module**: Manages the analysis pipeline, including interactions with language models and rendering outputs.
- **Pipeline/Parsers Module**: Extracts code structure using Tree-sitter.
- **Pipeline/Nodes Module**: Handles tasks like document validation, system overview generation, and repository data ingestion.
- **Pipeline/Prompts Module**: Provides prompt templates.

### Data Flow
- Data flows from the CLI module to the pipeline, where it is processed and analyzed. Results are rendered and outputted back through the CLI.

### Module Boundaries
- **CLI**: User interaction and configuration.
- **Pipeline**: Core processing and analysis.
- **Parsers**: Code structure extraction.
- **Nodes**: Task-specific processing.
- **Prompts**: Template management.

## 3. Behavioral Spec

### Pipeline Module
- **Intent**: Manage code-to-spec analysis pipeline.
- **Interfaces**: Various functions for LLM interaction, caching, and rendering.
- **Side Effects**: Writes to cache, interacts with LLMs.
- **Errors**: Raises exceptions on LLM call failures.

### Pipeline/Parsers Module
- **Intent**: Extract code structure.
- **Interfaces**: Functions for language determination and code parsing.
- **Side Effects**: None specified.
- **Errors**: None specified.

### Pipeline/Nodes Module
- **Intent**: Perform specific tasks within the pipeline.
- **Interfaces**: Functions for validation, synthesis, and analysis.
- **Side Effects**: Updates pipeline state.
- **Errors**: Raises exceptions on validation failures.

### CLI Module
- **Intent**: Provide a user interface for pipeline interaction.
- **Interfaces**: Functions for user prompts and pipeline execution.
- **Side Effects**: Displays output to the terminal.
- **Errors**: None specified.

## 4. Contracts

### Data Schemas
- **RunMemory**: Manages cross-run memory logs.
- **PipelineBuffer**: Manages pipeline execution state.
- **BehavioralTest**: Represents a behavioral test.
- **CrossCutting**: Represents cross-cutting concerns.
- **DataSchema**: Represents a data schema.
- **FileKind**: Represents the kind of a file.
- **FileMeta**: Represents metadata of a file.
- **Interface**: Represents an interface.
- **ModuleSummary**: Represents a summary of a module.
- **PipelineState**: Represents the state of the pipeline.
- **UnitAnalysis**: Represents an analysis of a code unit.
- **UnitAnalysisResult**: Represents the result of a unit analysis.

### API Surfaces
- Public interfaces are documented per module, detailing available functions and methods.

### Invariants
- None specified.

## 5. Cross-Cutting Concerns

### Error Handling
- Exceptions are raised for LLM call failures, file operation failures, and database operation failures.

### Configuration
- Managed through environment variables and Click for CLI parsing.

### Logging
- Implemented in `pipeline/indexer.py` and `pipeline/memory.py`.

### Auth
- Not specified.

### Concurrency
- Managed using `threading.BoundedSemaphore`.

### Integrations
- External packages include `click`, `pydantic`, `rich`, and various `langchain` modules.

## 6. Reimplementation Notes

- No specific idioms or idiomatic-equivalent guidance provided.

## 7. Acceptance Tests

### Given/When/Then Tests
- **BehavioralTest**: Produces documented results when called with valid inputs.
- **CLI Main**: Ingests codebase and produces a reimplementation spec when called with required inputs.
- **Pipeline Nodes Validate**: Raises an exception when LLM call fails.
- **Pipeline Nodes Generate Tests**: Returns generated behavioral tests when called with a valid `PipelineState`.
- **Pipeline LLM Call Structured**: Returns a validated schema instance when called with a prompt and schema.

This document provides a concise and accurate reimplementation specification based on the provided analysis results, adhering strictly to the grounding rules.

## Interface Index

_Complete list of public interfaces extracted from the source (ground truth)._

### `cli.py`
- **main** (function) — `main(repo: str, out: str, provider: str, model: str | None, ollama_url: str, max_parallelism: int, max_files: int | None, skip_tests: bool, analysis_passes: int, thread_id: str | None, langsmith_project: str | None, no_cache: bool, clear_cache: bool)`

### `cli/chat.py`
- **_format_context** (function) — `_format_context(docs) -> str`
- **_sources_line** (function) — `_sources_line(docs) -> str`
- **chat_repl** (function) — `chat_repl(collection: str, k: int = 8) -> None`

### `cli/main.py`
- **PipelineBuffer** (class) — `PipelineBuffer(max_messages: int = 100)`
- **__init__** (method) — `__init__(self, max_messages: int = 100)`
- **add_message** (method) — `add_message(self, msg_type: str, content: str) -> None`
- **set_node** (method) — `set_node(self, node_id: str, status: str) -> None`
- **complete_node** (method) — `complete_node(self, node_id: str) -> None`

### `cli/main.py`
- **_default** (function) — `_default(ctx: typer.Context) -> None`
- **create_layout** (function) — `create_layout() -> Layout`
- **update_display** (function) — `update_display(layout: Layout) -> None`
- **get_user_selections** (function) — `get_user_selections() -> dict`
- **step_box** (function) — `step_box(title: str, hint: str) -> None`
- **_safe_name** (function) — `_safe_name(path: str) -> str`
- **_persist_class_spec** (function) — `_persist_class_spec(ua) -> None`
- **_persist_stage_doc** (function) — `_persist_stage_doc(node_id: str, update: dict) -> None`
- **_pause** (function) — `_pause(message: str = 'Press Enter to return to the menu…') -> None`
- **_render_doc** (function) — `_render_doc(title: str, content: str) -> None`
- **interactive_viewer** (function) — `interactive_viewer(final_doc: str) -> None`
- **run_pipeline** (function) — `run_pipeline(no_cache: bool = False, clear_cache: bool = False) -> None`

### `cli/utils.py`
- **ask_repo_path** (function) — `ask_repo_path() -> str`
- **_valid** (function) — `_valid(val: str) -> bool | str`
- **ask_output_file** (function) — `ask_output_file() -> str`
- **ask_provider** (function) — `ask_provider() -> str`
- **ask_model** (function) — `ask_model(provider: str) -> str`
- **ask_ollama_model** (function) — `ask_ollama_model() -> str`
- **ask_max_files** (function) — `ask_max_files() -> int | None`
- **ask_skip_tests** (function) — `ask_skip_tests() -> bool`
- **ask_analysis_passes** (function) — `ask_analysis_passes() -> int`

### `graph.py`
- **route_to_units** (function) — `route_to_units(state: PipelineState) -> list[Send]`
- **should_refine_analysis** (function) — `should_refine_analysis(state: PipelineState)`
- **should_revise** (function) — `should_revise(state: PipelineState) -> str`
- **build_graph** (function) — `build_graph(checkpointer=None)`

### `pipeline/artifacts.py`
- **render_class_spec** (function) — `render_class_spec(ua) -> str`
- **render_stage_doc** (function) — `render_stage_doc(node_id: str, update: dict) -> str | None`
- **write_text** (function) — `write_text(path: Path, content: str) -> None`

### `pipeline/cache.py`
- **enabled** (function) — `enabled() -> bool`
- **cache_dir** (function) — `cache_dir() -> Path`
- **make_key** (function) — `make_key(*parts: str) -> str`
- **get** (function) — `get(key: str)`
- **set** (function) — `set(key: str, value) -> None`
- **clear** (function) — `clear() -> int`

### `pipeline/indexer.py`
- **_chunk** (function) — `_chunk(text: str, size: int = 1400, overlap: int = 150) -> list[str]`
- **_split_spec_sections** (function) — `_split_spec_sections(spec: str) -> list[tuple[str, str]]`
- **index_run** (function) — `index_run(repo_path: str, class_docs: dict[str, str], spec_text: str, log=print) -> tuple[str, int]`

### `pipeline/llm.py`
- **get_provider** (function) — `get_provider() -> str`
- **get_model_id** (function) — `get_model_id() -> str`
- **get_llm** (function) — `get_llm(temperature: float = 0)`
- **_invoke_with_retry** (function) — `_invoke_with_retry(llm, messages, max_conn_retries: int = 5)`
- **_extract_json_from_text** (function) — `_extract_json_from_text(text: str) -> str`
- **_try_repair_json** (function) — `_try_repair_json(text: str) -> str`
- **call_llm_json** (function) — `call_llm_json(prompt: str, max_retries: int = 2) -> dict | list`
- **_call_llm_json_uncached** (function) — `_call_llm_json_uncached(prompt: str, max_retries: int = 2) -> dict | list`
- **call_llm_structured** (function) — `call_llm_structured(prompt: str, schema, max_retries: int = 2)`
- **_call_llm_structured_uncached** (function) — `_call_llm_structured_uncached(prompt: str, schema, max_retries: int = 2)`
- **call_llm_text** (function) — `call_llm_text(prompt: str) -> str`

### `pipeline/memory.py`
- **RunMemory** (class) — `RunMemory(path: str | os.PathLike | None = None, max_entries: int | None = 50)`
- **__init__** (method) — `__init__(self, path: str | os.PathLike | None = None, max_entries: int | None = 50) -> None`
- **store_run** (method) — `store_run(self, repo_path: str, model: str, languages: list[str], unit_count: int, hallucinations: list[str], reflection: str = "") -> None`
- **_load_blocks** (method) — `_load_blocks(self) -> list[str]`
- **get_past_context** (method) — `get_past_context(self, repo_path: str, n: int = 3) -> str`
- **_rotate** (method) — `_rotate(self, blocks: list[str]) -> list[str]`

### `pipeline/model_catalog.py`
- **list_providers** (function) — `list_providers() -> list[tuple[str, str]]`
- **provider_config** (function) — `provider_config(provider: str) -> dict`
- **get_model_options** (function) — `get_model_options(provider: str) -> list[tuple[str, str]]`
- **default_model** (function) — `default_model(provider: str) -> str`

### `pipeline/nodes/analyze_unit.py`
- **_get_semaphore** (function) — `_get_semaphore(size: int) -> threading.BoundedSemaphore`
- **_elide** (function) — `_elide(source_bytes: bytes, ranges: list) -> str`
- **_select_source** (function) — `_select_source(state: dict) -> tuple[str, str]`
- **analyze_unit** (function) — `analyze_unit(state: dict) -> dict`

### `pipeline/nodes/assemble_document.py`
- **_build_inventory** (function) — `_build_inventory(state: PipelineState) -> str`
- **_build_interface_index** (function) — `_build_interface_index(state: PipelineState) -> str`
- **_insert_diagram** (function) — `_insert_diagram(doc: str, diagram: str) -> str`
- **assemble_document** (function) — `assemble_document(state: PipelineState) -> dict`

### `pipeline/nodes/extract_architecture.py`
- **_aggregate_evidence** (function) — `_aggregate_evidence(unit_analyses, dep_manifest) -> dict`
- **extract_architecture** (function) — `extract_architecture(state: PipelineState) -> dict`
- **_summary** (function) — `_summary(items: list[str], n: int = 5) -> str`

### `pipeline/nodes/generate_diagram.py`
- **_node_id** (function) — `_node_id(name: str) -> str`
- **_module_label** (function) — `_module_label(name: str) -> str`
- **_clean_label** (function) — `_clean_label(text: str, limit: int = 40) -> str`
- **_module_graph** (function) — `_module_graph(modules, entry_points) -> str | None`
- **_integrations_graph** (function) — `_integrations_graph(cross_cutting, system_label: str) -> str | None`
- **_member_name** (function) — `_member_name(name: str) -> str`
- **_field_type** (function) — `_field_type(prop) -> str`
- **_refs** (function) — `_refs(prop) -> set[str]`
- **_data_model** (function) — `_data_model(data_schemas) -> str | None`
- **generate_diagram** (function) — `generate_diagram(state: PipelineState) -> dict`

### `pipeline/nodes/generate_tests.py`
- **generate_tests** (function) — `generate_tests(state: PipelineState) -> dict`

### `pipeline/nodes/ingest.py`
- **_resolve_dependencies** (function) — `_resolve_dependencies(files: list[FileMeta]) -> None`
- **_exists** (function) — `_exists(base: str, exts: tuple[str, ...]) -> str | None`
- **_resolve_one** (function) — `_resolve_one(imp: str, language: str, file_dir: str) -> str | None`
- **_classify_kind** (function) — `_classify_kind(rel_path: str, ext: str) -> FileKind`
- **_extract_imports** (function) — `_extract_imports(source: str, language: str) -> list[str]`
- **_parse_requirements_txt** (function) — `_parse_requirements_txt(path: str) -> dict`
- **_parse_package_json** (function) — `_parse_package_json(path: str) -> dict`
- **_parse_go_mod** (function) — `_parse_go_mod(path: str) -> dict`
- **_parse_cargo_toml** (function) — `_parse_cargo_toml(path: str) -> dict`
- **_parse_pom_xml** (function) — `_parse_pom_xml(path: str) -> dict`
- **ingest** (function) — `ingest() -> None`

### `pipeline/nodes/reduce_modules.py`
- **reduce_modules** (function) — `reduce_modules(state: PipelineState) -> dict`

### `pipeline/nodes/review_completeness.py`
- **review_completeness** (function) — `review_completeness(state: PipelineState) -> dict`

### `pipeline/nodes/review_consistency.py`
- **_build_ground_truth** (function) — `_build_ground_truth(state: PipelineState) -> str`
- **review_consistency** (function) — `review_consistency(state: PipelineState) -> dict`

### `pipeline/nodes/route_units.py`
- **_file_units** (function) — `_file_units(file_meta, repo_path: str, max_parallelism: int) -> list[dict]`
- **route_units** (function) — `route_units(state: PipelineState) -> dict`

### `pipeline/nodes/synthesize_system.py`
- **synthesize_system** (function) — `synthesize_system(state: PipelineState) -> dict`

### `pipeline/nodes/validate.py`
- **validate** (function) — `validate(state: PipelineState) -> dict`

### `pipeline/parsers/tree_sitter_parser.py`
- **_get_lang_from_path** (function) — `_get_lang_from_path(path: str) -> str | None`
- **_get_ts_parser** (function) — `_get_ts_parser(language: str)`
- **_extract_go_imports** (function) — `_extract_go_imports(source: str) -> list[str]`
- **_extract_imports_regex** (function) — `_extract_imports_regex(source: str, language: str) -> list[str]`
- **_count_loc** (function) — `_count_loc(source: str) -> int`
- **_structure** (function) — `_structure(functions: list, classes: list, imports: list, loc: int) -> dict`
- **_empty_structure** (function) — `_empty_structure(source: str) -> dict`
- **_first_name** (function) — `_first_name(node, source_bytes: bytes) -> str | None`
- **_traverse_for_names** (function) — `_traverse_for_names(node, source_bytes: bytes, functions: list, classes: list)`
- **_collect_class_spans** (function) — `_collect_class_spans(node, source_bytes: bytes, out: list, inside_class: bool = False) -> None`
- **extract_class_spans** (function) — `extract_class_spans(path: str) -> list[dict]`
- **parse_file** (function) — `parse_file(path: str)`

### `pipeline/rag.py`
- **__init__** (method) — `__init__(self)`
- **add** (method) — `add(self, items: list[tuple[str, str]]) -> None`
- **retrieve** (method) — `retrieve(self, query: str, k: int)`
- **select_context** (function) — `select_context(full_text: str, records: list[dict], query: str, char_budget: int = RAG_CHAR_BUDGET, k: int = 12) -> tuple[str, bool]`

### `pipeline/reflection.py`
- **reflect_on_run** (function) — `reflect_on_run(repo_name: str, languages: list[str], unit_count: int, hallucinations: list[str]) -> str`

### `pipeline/repo_source.py`
- **is_git_url** (function) — `is_git_url(source: str) -> bool`
- **_clone_dir_name** (function) — `_clone_dir_name(url: str) -> str`
- **_normalize_url** (function) — `_normalize_url(url: str) -> str`
- **resolve_repo_source** (function) — `resolve_repo_source(source: str, log=print, force_fresh: bool = False) -> str`

### `pipeline/vectordb.py`
- **get_conn_string** (function) — `get_conn_string() -> str`
- **get_embeddings** (function) — `get_embeddings()`
- **collection_for** (function) — `collection_for(repo_path: str) -> str`
- **get_store** (function) — `get_store(collection: str, embed_meta: dict | None = None)`
- **_provider_from_dim** (function) — `_provider_from_dim(dim: int) -> dict | None`
- **collection_embed_config** (function) — `collection_embed_config(collection: str) -> dict | None`
- **_raw_conn_string** (function) — `_raw_conn_string() -> str`
- **check_connection** (function) — `check_connection() -> tuple[bool, str]`
- **list_collections** (function) — `list_collections() -> list[str]`

### `state_schema.py`
- **merge_unit_analyses** (function) — `merge_unit_analyses(existing, new)`
- **FileKind** (class) — `class FileKind(str, Enum)`
- **FileMeta** (class) — `class FileMeta(BaseModel)`
- **Interface** (class) — `class Interface(BaseModel)`
- **UnitAnalysis** (class) — `class UnitAnalysis(BaseModel)`
- **UnitAnalysisResult** (class) — `class UnitAnalysisResult(BaseModel)`
- **ModuleSummary** (class) — `class ModuleSummary(BaseModel)`
- **DataSchema** (class) — `class DataSchema(BaseModel)`
- **CrossCutting** (class) — `class CrossCutting(BaseModel)`
- **BehavioralTest** (class) — `class BehavioralTest(BaseModel)`
- **PipelineState** (class) — `class PipelineState(TypedDict, total=False)`
