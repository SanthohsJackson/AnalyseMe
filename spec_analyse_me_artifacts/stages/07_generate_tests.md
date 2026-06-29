# Stage: Test Generation

**Acceptance tests:** 107

### pipeline/nodes/validate.validate
- **Given:** A PipelineState object with unit analyses and a draft document.
- **When:** The validate function is called with the PipelineState.
- **Then:** A dictionary is returned containing validation results, gaps, and the final document.

### pipeline/nodes/validate.validate
- **Given:** A PipelineState object with unit analyses and a draft document.
- **When:** The validate function is called and the LLM call fails.
- **Then:** An Exception is raised.

### pipeline/reflection.reflect_on_run
- **Given:** A repository name, a list of programming languages, a unit count, and a list of hallucinations.
- **When:** The reflect_on_run function is called with these inputs.
- **Then:** A string is returned containing a concise reflection or an empty string on failure.

### pipeline/nodes/synthesize_system.synthesize_system
- **Given:** A PipelineState object containing module summaries and a repo path.
- **When:** The synthesize_system function is called with the PipelineState.
- **Then:** A dictionary is returned containing the system overview as 'system_overview'.

### pipeline/nodes/generate_tests.generate_tests
- **Given:** A PipelineState object containing unit analyses.
- **When:** The generate_tests function is called with the PipelineState.
- **Then:** A dictionary is returned containing generated behavioral tests.

### pipeline/nodes/extract_architecture.extract_architecture
- **Given:** A PipelineState object containing module summaries.
- **When:** The extract_architecture function is called with the PipelineState.
- **Then:** A dictionary is returned containing derived data schemas and cross-cutting concerns.

### pipeline/rag.__init__
- **Given:** No preconditions.
- **When:** The RAGIndex is initialized.
- **Then:** An in-memory vector store for embeddings is initialized.

### pipeline/rag.add
- **Given:** A list of (id, text) tuples.
- **When:** The add method is called with the list of tuples.
- **Then:** The documents are added to the in-memory vector store.

### pipeline/rag.retrieve
- **Given:** A query string and an integer k.
- **When:** The retrieve method is called with the query and k.
- **Then:** A list of the top-k documents matching the query is returned.

### pipeline/rag.select_context
- **Given:** Full text, a list of records, a query, a character budget, and an integer k.
- **When:** The select_context function is called with these inputs.
- **Then:** A tuple is returned containing the context text and a flag indicating if RAG was used.

### pipeline/rag.select_context
- **Given:** Embeddings/store are unavailable.
- **When:** The select_context function is called.
- **Then:** An Exception is raised.

### pipeline/cache.enabled
- **Given:** No preconditions.
- **When:** The enabled function is called.
- **Then:** A boolean is returned indicating whether the cache is enabled.

### pipeline/cache.cache_dir
- **Given:** No preconditions.
- **When:** The cache_dir function is called.
- **Then:** A Path is returned for the cache directory, and the directory is created if it does not exist.

### pipeline/cache.make_key
- **Given:** A set of string parts.
- **When:** The make_key function is called with the parts.
- **Then:** A SHA-256 hash of the input parts is returned as a string.

### pipeline/cache.get
- **Given:** A cache key.
- **When:** The get function is called with the key.
- **Then:** The cached value is returned or None if not found.

### pipeline/cache.set
- **Given:** A cache key and a JSON-serializable value.
- **When:** The set function is called with the key and value.
- **Then:** The value is stored in the cache under the specified key.

### pipeline/cache.clear
- **Given:** No preconditions.
- **When:** The clear function is called.
- **Then:** All entries are removed from the cache, and the number of cache files removed is returned.

### pipeline/nodes/review_consistency.review_consistency
- **Given:** A PipelineState object containing the draft document and analyses.
- **When:** The review_consistency function is called with the PipelineState.
- **Then:** A dictionary is returned with the result of the review, including pass status and findings.

### pipeline/nodes/route_units.route_units
- **Given:** A PipelineState object representing the current state of the pipeline.
- **When:** The route_units function is called with the PipelineState.
- **Then:** A dictionary is returned containing units to analyze, and the number of units queued is printed.

### pipeline/repo_source.is_git_url
- **Given:** A source string.
- **When:** The is_git_url function is called with the source string.
- **Then:** A boolean is returned indicating whether the source is a git URL.

### pipeline/repo_source.resolve_repo_source
- **Given:** A source string, a logging function, and a force_fresh flag.
- **When:** The resolve_repo_source function is called with these inputs.
- **Then:** A string is returned representing the local directory path for the resolved source.

### pipeline/repo_source.resolve_repo_source
- **Given:** The source is neither a directory nor a recognized git URL.
- **When:** The resolve_repo_source function is called.
- **Then:** A ValueError is raised.

### pipeline/repo_source.resolve_repo_source
- **Given:** A git clone operation fails.
- **When:** The resolve_repo_source function is called.
- **Then:** A RuntimeError is raised.

### pipeline/nodes/review_completeness.review_completeness
- **Given:** A PipelineState object including unit analyses and repo path.
- **When:** The review_completeness function is called with the PipelineState.
- **Then:** A dictionary is returned containing analysis questions, completeness status, and pass number.

### cli/chat.chat_repl
- **Given:** A collection name and an integer k.
- **When:** The chat_repl function is called with these inputs.
- **Then:** An interactive Q&A loop is run, querying an indexed collection with a local LLM, and results are printed to the console.

### pipeline/indexer.index_run
- **Given:** A repository path, a dictionary of class documentation, a specification text, and a logging function.
- **When:** The index_run function is called with these inputs.
- **Then:** A tuple is returned containing the collection name and document count.

### pipeline/nodes/reduce_modules.py.reduce_modules
- **Given:** A PipelineState object with unit analyses grouped by directory
- **When:** reduce_modules is called with the PipelineState
- **Then:** A dictionary containing module summaries is returned

### pipeline/memory.py.RunMemory
- **Given:** A valid file path and a maximum number of entries
- **When:** A RunMemory instance is initialized with these parameters
- **Then:** The instance is set up with the specified path and entry limit

### pipeline/memory.py.store_run
- **Given:** A RunMemory instance and details of a run including repo_path, model, languages, unit_count, hallucinations, and reflection
- **When:** store_run is called with these details
- **Then:** The run entry is appended to the memory log

### pipeline/memory.py._load_blocks
- **Given:** A RunMemory instance with a memory log file
- **When:** _load_blocks is called
- **Then:** A list of memory log blocks is returned

### pipeline/memory.py.get_past_context
- **Given:** A RunMemory instance with past run entries for a specific repository
- **When:** get_past_context is called with the repository path and a number of past entries to retrieve
- **Then:** A formatted string of lessons from past runs is returned

### pipeline/memory.py._rotate
- **Given:** A RunMemory instance with a list of memory log blocks exceeding the maximum number of entries
- **When:** _rotate is called with the list of blocks
- **Then:** A rotated list of memory log blocks is returned, ensuring the maximum number of entries is not exceeded

### graph.py.route_to_units
- **Given:** A PipelineState object with unit descriptors
- **When:** route_to_units is called with the PipelineState
- **Then:** A list of Send objects for each unit descriptor is returned

### graph.py.should_refine_analysis
- **Given:** A PipelineState object with flagged units
- **When:** should_refine_analysis is called with the PipelineState
- **Then:** A list of Send objects for re-analysis or 'reduce_modules' is returned

### graph.py.should_revise
- **Given:** A PipelineState object with validation and review results
- **When:** should_revise is called with the PipelineState
- **Then:** A string 'assemble_document' or 'END' is returned

### pipeline/model_catalog.py.list_providers
- **Given:** No preconditions
- **When:** list_providers is called
- **Then:** A list of tuples containing provider keys and their labels is returned

### pipeline/model_catalog.py.provider_config
- **Given:** A valid provider key
- **When:** provider_config is called with the provider key
- **Then:** A dictionary containing configuration details of the specified provider is returned

### pipeline/model_catalog.py.get_model_options
- **Given:** A valid provider key
- **When:** get_model_options is called with the provider key
- **Then:** A list of tuples containing model options for the specified provider is returned

### pipeline/model_catalog.py.default_model
- **Given:** A valid provider key
- **When:** default_model is called with the provider key
- **Then:** The default model identifier for the specified provider is returned

### pipeline/nodes/analyze_unit.py.analyze_unit
- **Given:** A unit descriptor with analysis parameters
- **When:** analyze_unit is called with the unit descriptor
- **Then:** A dictionary containing unit analyses and any mapping errors is returned

### cli.py.main
- **Given:** All required inputs including repo, out, provider, ollama_url, max_parallelism, skip_tests, analysis_passes, and no_cache
- **When:** main is called with these inputs
- **Then:** The codebase is analyzed and a language-agnostic reimplementation spec is produced, with status and progress messages printed

### pipeline/vectordb.py.get_conn_string
- **Given:** Environment variables set for PostgreSQL connection
- **When:** get_conn_string is called
- **Then:** The connection string for the PostgreSQL database is returned

### pipeline/vectordb.py.collection_for
- **Given:** A valid repository path
- **When:** collection_for is called with the repository path
- **Then:** A stable, unique collection name is returned

### pipeline/vectordb.py.check_connection
- **Given:** Database connection parameters are set
- **When:** check_connection is called
- **Then:** A tuple containing the connection status and a message is returned

### cli/utils.py.ask_repo_path
- **Given:** No repository path or URL provided
- **When:** ask_repo_path is called
- **Then:** The program exits if no repository is provided

### cli/utils.py._valid
- **Given:** a valid directory path as input
- **When:** the _valid function is called with the directory path
- **Then:** the function returns True

### cli/utils.py._valid
- **Given:** a valid git URL as input
- **When:** the _valid function is called with the git URL
- **Then:** the function returns True

### cli/utils.py._valid
- **Given:** an invalid directory path or git URL as input
- **When:** the _valid function is called with the invalid input
- **Then:** the function returns an error message

### cli/utils.py.ask_output_file
- **Given:** no preconditions
- **When:** the ask_output_file function is called
- **Then:** the function returns the name of the output file

### cli/utils.py.ask_provider
- **Given:** no preconditions
- **When:** the ask_provider function is called
- **Then:** the function returns the selected LLM provider

### cli/utils.py.ask_model
- **Given:** a valid provider string
- **When:** the ask_model function is called with the provider
- **Then:** the function returns the selected model for the provider

### cli/utils.py.ask_ollama_model
- **Given:** no preconditions
- **When:** the ask_ollama_model function is called
- **Then:** the function returns the selected Ollama model

### cli/utils.py.ask_max_files
- **Given:** no preconditions
- **When:** the ask_max_files function is called
- **Then:** the function returns an integer file cap or None

### cli/utils.py.ask_skip_tests
- **Given:** no preconditions
- **When:** the ask_skip_tests function is called
- **Then:** the function returns a boolean indicating whether to skip test files

### cli/utils.py.ask_analysis_passes
- **Given:** no preconditions
- **When:** the ask_analysis_passes function is called
- **Then:** the function returns the number of analysis refinement passes

### state_schema.py.merge_unit_analyses
- **Given:** two lists of UnitAnalysis objects with some overlapping unit_ids
- **When:** the merge_unit_analyses function is called with the two lists
- **Then:** the function returns a list where the latest analysis replaces any previous one for overlapping unit_ids

### pipeline/nodes/assemble_document.py._build_inventory
- **Given:** a PipelineState object containing analysis data
- **When:** the _build_inventory function is called with the PipelineState
- **Then:** the function returns a formatted inventory of files, languages, entry points, and dependencies

### pipeline/nodes/assemble_document.py._insert_diagram
- **Given:** a document string containing an 'Architecture' heading and a diagram string
- **When:** the _insert_diagram function is called with the document and diagram
- **Then:** the function returns the document with the diagram inserted after the 'Architecture' heading

### pipeline/nodes/assemble_document.py.assemble_document
- **Given:** a PipelineState object containing analysis data
- **When:** the assemble_document function is called with the PipelineState
- **Then:** the function returns a dictionary containing the draft document and updated revision count

### pipeline/nodes/generate_diagram.py._node_id
- **Given:** a name string
- **When:** the _node_id function is called with the name
- **Then:** the function returns a stable, Mermaid-safe node id

### pipeline/nodes/generate_diagram.py._module_label
- **Given:** a module name string
- **When:** the _module_label function is called with the module name
- **Then:** the function returns a label for the module, using '(root)' for the root module

### pipeline/nodes/generate_diagram.py._clean_label
- **Given:** a text string and a limit integer
- **When:** the _clean_label function is called with the text and limit
- **Then:** the function returns a cleaned and possibly truncated label

### pipeline/nodes/generate_diagram.py._module_graph
- **Given:** a list of module objects and a list of entry point paths
- **When:** the _module_graph function is called with the modules and entry points
- **Then:** the function returns a Mermaid graph definition or None if no modules

### pipeline/nodes/generate_diagram.py._integrations_graph
- **Given:** an object containing external integrations and a system label string
- **When:** the _integrations_graph function is called with the cross_cutting object and system label
- **Then:** the function returns a Mermaid graph definition or None if no integrations

### pipeline/nodes/generate_diagram.py._member_name
- **Given:** a name string
- **When:** the _member_name function is called with the name
- **Then:** the function returns a sanitized member name

### pipeline/nodes/generate_diagram.py._field_type
- **Given:** a JSON-schema property dictionary
- **When:** the _field_type function is called with the property
- **Then:** the function returns a human-readable type description

### pipeline/nodes/generate_diagram.py._refs
- **Given:** a JSON-schema property dictionary
- **When:** the _refs function is called with the property
- **Then:** the function returns a set of schema names referenced by the property

### pipeline/nodes/generate_diagram._data_model
- **Given:** a list of data schema objects is provided
- **When:** the _data_model function is called with the list
- **Then:** a Mermaid class diagram string is returned

### pipeline/nodes/generate_diagram._data_model
- **Given:** an empty list of data schema objects is provided
- **When:** the _data_model function is called with the list
- **Then:** None is returned

### pipeline/nodes/generate_diagram.generate_diagram
- **Given:** a PipelineState object containing analysis data is provided
- **When:** the generate_diagram function is called with the PipelineState
- **Then:** a dictionary containing the architecture diagram is returned

### pipeline/llm.get_provider
- **Given:** environment variables are set with an active LLM provider key
- **When:** the get_provider function is called
- **Then:** the active LLM provider key is returned as a string

### pipeline/llm.get_model_id
- **Given:** environment variables or provider defaults are available
- **When:** the get_model_id function is called
- **Then:** the resolved chat model id is returned as a string

### pipeline/llm._invoke_with_retry
- **Given:** an LLM client and messages are provided, and the LLM provider is reachable
- **When:** the _invoke_with_retry function is called with max_conn_retries set to 5
- **Then:** the LLM is invoked successfully without raising a RuntimeError

### pipeline/llm._invoke_with_retry
- **Given:** an LLM client and messages are provided, and the LLM provider is unreachable
- **When:** the _invoke_with_retry function is called with max_conn_retries set to 5
- **Then:** a RuntimeError is raised after retries

### pipeline/llm._extract_json_from_text
- **Given:** a string containing JSON within markdown code fences is provided
- **When:** the _extract_json_from_text function is called with the string
- **Then:** the raw JSON text is extracted and returned as a string

### pipeline/llm._try_repair_json
- **Given:** a string containing potentially truncated JSON is provided
- **When:** the _try_repair_json function is called with the string
- **Then:** the repaired JSON text is returned as a string

### pipeline/llm.call_llm_json
- **Given:** a prompt string is provided and valid JSON can be obtained
- **When:** the call_llm_json function is called with the prompt and max_retries set to 2
- **Then:** a parsed JSON object or array is returned

### pipeline/llm.call_llm_json
- **Given:** a prompt string is provided and valid JSON cannot be obtained
- **When:** the call_llm_json function is called with the prompt and max_retries set to 2
- **Then:** a ValueError is raised

### pipeline/llm.call_llm_text
- **Given:** a prompt string is provided
- **When:** the call_llm_text function is called with the prompt
- **Then:** the raw text response from the LLM is returned as a string

### pipeline/artifacts.render_class_spec
- **Given:** a UnitAnalysis object is provided
- **When:** the render_class_spec function is called with the UnitAnalysis
- **Then:** a Markdown representation of the unit analysis is returned as a string

### pipeline/artifacts.render_stage_doc
- **Given:** a node_id string and a state update dictionary are provided
- **When:** the render_stage_doc function is called with the node_id and update
- **Then:** a Markdown document for the stage is returned as a string or None if not applicable

### pipeline/artifacts.write_text
- **Given:** a file path and text content are provided
- **When:** the write_text function is called with the path and content
- **Then:** the content is written to a file at the specified path

### pipeline/parsers/tree_sitter_parser._get_lang_from_path
- **Given:** a file path with a known extension is provided
- **When:** the _get_lang_from_path function is called with the path
- **Then:** the language name is returned as a string

### pipeline/parsers/tree_sitter_parser._get_lang_from_path
- **Given:** a file path with an unknown extension is provided
- **When:** the _get_lang_from_path function is called with the path
- **Then:** None is returned

### pipeline/parsers/tree_sitter_parser._extract_go_imports
- **Given:** Go source code containing import paths is provided
- **When:** the _extract_go_imports function is called with the source code
- **Then:** a list of Go import paths is returned

### pipeline/parsers/tree_sitter_parser._count_loc
- **Given:** source code is provided
- **When:** the _count_loc function is called with the source code
- **Then:** the number of non-blank lines is returned as an integer

### pipeline/parsers/tree_sitter_parser._structure
- **Given:** lists of functions, classes, imports, and a LOC count are provided
- **When:** the _structure function is called with the lists and LOC count
- **Then:** a structured representation of the code is returned as a dictionary

### pipeline/parsers/tree_sitter_parser._empty_structure
- **Given:** source code is provided
- **When:** the _empty_structure function is called with the source code
- **Then:** an empty structure with LOC count is returned as a dictionary

### pipeline/parsers/tree_sitter_parser.extract_class_spans
- **Given:** a file path is provided
- **When:** the extract_class_spans function is called with the path
- **Then:** a list of class spans with byte and line information is returned

### pipeline/nodes/ingest._resolve_dependencies
- **Given:** a list of FileMeta objects is provided
- **When:** the _resolve_dependencies function is called with the list
- **Then:** internal dependencies for files are resolved

### pipeline/nodes/ingest._exists
- **Given:** a base path and a tuple of file extensions are provided
- **When:** the _exists function is called with the base path and extensions
- **Then:** the resolved path is returned as a string if it exists, otherwise None

### pipeline/nodes/ingest.py._resolve_one
- **Given:** An import statement, a programming language, and a file directory are provided.
- **When:** The _resolve_one function is called with these inputs.
- **Then:** The function returns the resolved file path if it exists, otherwise it returns None.

### pipeline/nodes/ingest.py._classify_kind
- **Given:** A relative file path and a file extension are provided.
- **When:** The _classify_kind function is called with these inputs.
- **Then:** The function returns the classification of the file kind as a FileKind object.

### pipeline/nodes/ingest.py._extract_imports
- **Given:** Source code and a programming language are provided.
- **When:** The _extract_imports function is called with these inputs.
- **Then:** The function returns a list of extracted import statements from the source code.

### pipeline/nodes/ingest.py._parse_requirements_txt
- **Given:** A path to a requirements.txt file is provided.
- **When:** The _parse_requirements_txt function is called with this input.
- **Then:** The function returns a dictionary containing the type and dependencies extracted from the file.

### pipeline/nodes/ingest.py._parse_package_json
- **Given:** A path to a package.json file is provided.
- **When:** The _parse_package_json function is called with this input.
- **Then:** The function returns a dictionary containing package information and dependencies extracted from the file.

### pipeline/nodes/ingest.py._parse_go_mod
- **Given:** A path to a go.mod file is provided.
- **When:** The _parse_go_mod function is called with this input.
- **Then:** The function returns a dictionary containing the module name and dependencies extracted from the file.

### pipeline/nodes/ingest.py._parse_cargo_toml
- **Given:** A path to a Cargo.toml file is provided.
- **When:** The _parse_cargo_toml function is called with this input.
- **Then:** The function returns a dictionary containing dependencies extracted from the file.

### pipeline/nodes/ingest.py._parse_pom_xml
- **Given:** A path to a pom.xml file is provided.
- **When:** The _parse_pom_xml function is called with this input.
- **Then:** The function returns a dictionary containing dependencies extracted from the file.

### pipeline/nodes/ingest.py.ingest
- **Given:** The repository is set up with files and dependency manifests.
- **When:** The ingest function is called.
- **Then:** The function walks the repository, classifies files, parses dependency manifests, and detects entry points.

### cli/main.py.PipelineBuffer.__init__
- **Given:** A maximum number of messages is provided.
- **When:** The PipelineBuffer is initialized with this input.
- **Then:** The message buffer and node status tracking are initialized.

### cli/main.py.PipelineBuffer.add_message
- **Given:** A message type and content are provided.
- **When:** The add_message method is called with these inputs.
- **Then:** A timestamped message is appended to the message buffer.

### cli/main.py.PipelineBuffer.set_node
- **Given:** A node identifier and a status are provided.
- **When:** The set_node method is called with these inputs.
- **Then:** The status of the node is updated and set as the current node if in progress.

### cli/main.py.PipelineBuffer.complete_node
- **Given:** A node identifier is provided.
- **When:** The complete_node method is called with this input.
- **Then:** The node is marked as completed.

### cli/main.py.create_layout
- **Given:** The terminal UI needs a layout structure.
- **When:** The create_layout function is called.
- **Then:** The function returns a configured layout for the terminal UI.

### cli/main.py.get_user_selections
- **Given:** The pipeline configuration needs user input.
- **When:** The get_user_selections function is called.
- **Then:** The function returns a dictionary of user selections for pipeline configuration.

### cli/main.py._safe_name
- **Given:** A unit path is provided.
- **When:** The _safe_name function is called with this input.
- **Then:** The function returns a filename-safe string derived from the path.
