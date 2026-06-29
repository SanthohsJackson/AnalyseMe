# Analyse Me

**Analyse Me** ingests any codebase and produces a **language-agnostic reimplementation spec** — a document detailed enough that an engineer (or another LLM) could rebuild the system in a different language without seeing the original source.

It is built on [LangGraph](https://langchain-ai.github.io/langgraph/): the codebase is parsed into units, each unit is analysed in parallel, the results are reduced and synthesised into a system-level spec, and the draft is checked by an anti-hallucination reviewer and a coverage critic before it's accepted. After a run you can browse every artifact and **chat with the codebase** via RAG.

---

## How it works

The pipeline is a `StateGraph` (see [graph.py](graph.py)) that runs these stages in order:

| Stage | Node | What it does |
|-------|------|--------------|
| Ingestion | `ingest` | Walks the repo, detects languages, collects source files (optionally skipping tests / capping file count). |
| Routing | `route_units` | Splits files into analysis **units** (large files are chunked) and fans them out. |
| Unit Analysis | `analyze_unit` | Analyses each unit in parallel (up to `--max-parallelism`) into a per-unit spec. |
| Completeness | `review_completeness` | Flags under-captured units and asks follow-up questions; can loop back to re-analyse for N passes. |
| Module Reduction | `reduce_modules` | Summarises units into module-level descriptions. |
| System Synthesis | `synthesize_system` | Produces the system overview from the module summaries. |
| Architecture | `extract_architecture` | Extracts data schemas, interfaces, and dependencies. |
| Test Generation | `generate_tests` | Derives behavioural / acceptance tests from the analysis. |
| Diagram | `generate_diagram` | Builds a Mermaid architecture diagram. |
| Assembly | `assemble_document` | Assembles all of the above into a single draft spec. |
| Review | `review_consistency` | **Anti-hallucination** pass: flags claims in the draft not grounded in the analysis. |
| Validation | `validate` | **Coverage critic**: checks the spec covers the codebase. |

The document is only accepted when **both** the consistency review and the validation critic pass; otherwise it loops back to re-assemble (up to `MAX_REVISIONS`). Lessons from each run (e.g. hallucinations caught) are stored and fed into future runs of the same repo.

### Inputs & outputs

- **Input:** a local path *or* a git URL (e.g. `https://github.com/owner/repo`).
- **Output:** a spec file (default `spec.md`) plus a `<name>_artifacts/` folder containing per-stage docs and per-unit specs.

### Providers

LLM access goes through a single catalog ([pipeline/model_catalog.py](pipeline/model_catalog.py)). Supported providers: **Ollama** (local, default), **OpenAI**, **DeepSeek**, **OpenRouter**, **xAI**, **Groq**, **Together**. Most hosted providers use the OpenAI-compatible path — adding one is a single row in the catalog.

---

## Setup

Requires **Python 3.11+**. (Optional: [Ollama](https://ollama.com) for local models, and Docker for the RAG chat vector DB.)

```bash
# 1. Clone
git clone https://github.com/SanthohsJackson/AnalyseMe.git
cd AnalyseMe

# 2. Create a venv and install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure (see Configuration below)
cp .env.example .env
# then edit .env and add the API key for your chosen provider
```

`run.sh` will also create the venv and install dependencies automatically on first run if you prefer.

---

## Configuration

Copy `.env.example` to `.env` and fill in the values for the provider you intend to use. Key settings:

| Variable | Purpose |
|----------|---------|
| `LLM_PROVIDER` | `ollama` (default), `openai`, `deepseek`, `openrouter`, `xai`, `groq`, `together`. |
| `OPENAI_API_KEY` (etc.) | API key matching your chosen provider. |
| `OLLAMA_BASE_URL` | Ollama endpoint (default `http://localhost:11434`). |
| `POSTGRES_CONN` | pgvector connection string for RAG chat (matches `docker-compose.yml`). |
| `OPENAI_EMBED_MODEL` / `OLLAMA_EMBED_MODEL` | Embedding model used for RAG indexing. |
| `LANGSMITH_API_KEY` | Optional — enables LangSmith tracing. |

> **Note:** `.env` is git-ignored and is **never** committed. Only `.env.example` (with no secrets) lives in the repo.

---

## Running

### Interactive UI (recommended)

```bash
./run.sh            # opens the startup menu (analyse vs chat)
./run.sh analyse    # jump straight to the analysis wizard
./run.sh chat       # chat about a previously-indexed codebase
```

The wizard walks you through repo, output file, provider, model, file cap, test handling, and analysis passes, then shows a live dashboard of pipeline progress with a spec preview.

### Headless CLI

```bash
python cli.py --repo https://github.com/owner/repo --out spec.md \
    --provider openai --model gpt-4o-mini
```

Useful flags (`python cli.py --help` for the full list):

| Flag | Description |
|------|-------------|
| `--repo` | **(required)** Local path or git URL to analyse. |
| `--out` | Output spec path (default `spec.md`). |
| `--provider` / `--model` | LLM provider and model id. |
| `--max-parallelism` | Max parallel unit analyses (default 8). |
| `--max-files` | Cap files analysed — useful for large repos. |
| `--skip-tests` / `--include-tests` | Whether to analyse test files (default: skip). |
| `--analysis-passes` | Completeness-refinement passes (default 1). |
| `--thread-id` | Resume a previous run. |
| `--no-cache` / `--clear-cache` | Control the on-disk LLM response cache. |

---

## Chat with the codebase (RAG)

After a run you can index the code + generated spec into a [pgvector](https://github.com/pgvector/pgvector) database and chat with it.

```bash
# Start the vector DB (port 5433 on the host)
docker compose up -d

# Then choose "Index this run" after analysing, or:
./run.sh chat
```

Embeddings used for chat are auto-matched to whatever built the index, so retrieval stays consistent.

---

## Project layout

```
cli.py                 Headless CLI entry point
main.py                Entry point for the interactive UI (python main.py)
graph.py               LangGraph StateGraph wiring (the pipeline)
state_schema.py        Shared pipeline state definition
cli/                   Rich terminal UI, wizard, and chat REPL
pipeline/
  nodes/               One module per pipeline stage
  parsers/             Tree-sitter based code parsing
  prompts/             LLM prompts
  model_catalog.py     Providers + model defaults
  rag.py, vectordb.py, indexer.py   RAG chat + pgvector indexing
  cache.py, memory.py, reflection.py   LLM cache + cross-run memory
docker-compose.yml     pgvector service for RAG chat
tests/                 Test suite
```

## Testing

```bash
pytest
```
