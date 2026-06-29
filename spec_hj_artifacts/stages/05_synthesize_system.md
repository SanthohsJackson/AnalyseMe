# Stage: System Synthesis

### Overview

AnalyseMe is a code analysis tool designed to generate language-agnostic specifications from code repositories. It addresses the need for automated code-to-spec analysis by providing a comprehensive pipeline that extracts code structure, manages repository data, and interacts with language models to produce detailed documentation and insights. The system facilitates user interaction through a command-line interface, enabling users to configure and execute analysis pipelines efficiently.

### How It Works

1. **Entry Points**: Execution begins at one of the three entry points: `cli.py`, `main.py`, or `cli/main.py`. These scripts initialize the application and set up the environment for analysis.

2. **CLI Interaction**: If initiated via the CLI, the `cli` module manages user interaction. It provides a command-line interface for configuring the analysis pipeline, querying the repository, and displaying results. The user can select models, specify repository paths, and manage pipeline execution through interactive prompts.

3. **Pipeline Execution**: The `pipeline` module is central to the analysis process. It manages tasks such as code-to-spec analysis, interaction with language models, and documentation generation. It also handles caching, retrieval-augmented generation, and indexing runs into a vector database.

4. **Code Structure Extraction**: The `pipeline/parsers` module extracts code structure using Tree-sitter. It determines programming languages, retrieves parsers, and builds structured representations of code, which are essential for subsequent analysis steps.

5. **Analysis and Documentation**: The `pipeline/nodes` module performs various tasks, including validating documents, generating tests, and extracting architecture. It synthesizes system overviews and assembles documents, collaborating with the `pipeline` and `pipeline/parsers` modules to ensure comprehensive analysis.

6. **Prompt Management**: The `pipeline/prompts` module defines prompt templates used in the code-to-spec pipeline, facilitating interactions with language models.

7. **Execution Management**: The `.` module serves as the overarching entry point, managing the state graph for the analysis pipeline and defining data structures for representing code units.

### Key Components

- **pipeline**: Manages the core analysis tasks, including interaction with language models, caching, and documentation generation.
- **pipeline/parsers**: Extracts code structure using Tree-sitter, determining programming languages and building structured code representations.
- **pipeline/nodes**: Handles document validation, test generation, architecture extraction, and document assembly, collaborating with other modules for comprehensive analysis.
- **pipeline/prompts**: Defines prompt templates for interactions with language models, supporting the code-to-spec pipeline.
- **cli**: Provides a command-line interface for configuring and executing the analysis pipeline, managing user interaction and displaying results.
- **.**: Acts as the main entry point, managing the analysis pipeline's state and defining language-agnostic data structures for code representation.