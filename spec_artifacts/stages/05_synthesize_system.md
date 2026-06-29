# Stage: System Synthesis

### Overview

The 'AnalyseMe' project is a code analysis tool designed to generate language-agnostic specifications from code repositories. It addresses the need for automated code-to-spec analysis by facilitating tasks such as code structure extraction, repository indexing, and interaction with language models. The system provides a command-line interface for configuring and managing analysis pipelines, enabling users to query and interact with code repositories efficiently.

### How It Works

1. **Entry Points**: Execution begins at one of the three entry points: `cli.py`, `main.py`, or `cli/main.py`. These scripts initialize the application and set up the environment for analysis.

2. **CLI Interaction**: If initiated via the CLI, the `cli` module manages user interaction. It provides utilities for configuring the analysis pipeline, querying repositories, and displaying results through a terminal interface. The CLI interacts with the `pipeline` and `pipeline/prompts` modules to facilitate these tasks.

3. **Pipeline Execution**: The `pipeline` module is central to the analysis process. It manages tasks such as code-to-spec analysis, interaction with language models, and documentation generation. It collaborates with the `pipeline/nodes` module to perform specific tasks like validating documents, generating tests, and extracting architecture.

4. **Code Structure Extraction**: The `pipeline/parsers` module extracts code structure using Tree-sitter, determining programming languages, and building structured representations of code. This module operates independently without direct collaboration with other modules.

5. **Data Management**: The `pipeline` module also handles data management tasks, including caching, indexing runs into a vector database, and maintaining logs of past analyses.

6. **Analysis and Documentation**: The `pipeline/nodes` module executes various analysis tasks and collaborates with the `pipeline` module to synthesize system overviews and generate documentation.

### Key Components

- **pipeline**: Facilitates code-to-spec analysis, manages interactions with language models, and renders outputs to Markdown. It is the core module for executing and managing the analysis pipeline.

- **pipeline/parsers**: Responsible for extracting code structure using Tree-sitter, determining programming languages, and building structured code representations.

- **pipeline/nodes**: Contains scripts for specific tasks within the pipeline, such as validating documents, generating tests, and extracting architecture. It collaborates with the `pipeline` module to perform these tasks.

- **pipeline/prompts**: Defines prompt templates for the code-to-spec pipeline, aiding in the interaction with language models.

- **cli**: Provides a command-line interface for configuring and managing the analysis pipeline, querying repositories, and displaying results. It interacts with the `pipeline` and `pipeline/prompts` modules.

- **.**: Serves as the entry point for executing the CLI application, managing the analysis pipeline, and defining data structures for code units. It collaborates with the `cli`, `pipeline`, and `pipeline/nodes` modules.