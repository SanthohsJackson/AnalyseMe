"""CLI entry point for the Analyse Me pipeline."""

import os
import uuid
from pathlib import Path

import click

# Load .env from project root if present
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
from langgraph.checkpoint.memory import MemorySaver

from graph import build_graph


@click.command()
@click.option("--repo", required=True, help="Local path OR git URL (e.g. https://github.com/owner/repo) to analyze")
@click.option("--out", default="spec.md", help="Output file path")
@click.option("--provider", default="ollama", help="LLM provider (ollama, openai, deepseek, openrouter, xai, groq, together)")
@click.option("--model", default=None, help="Model id (defaults to the provider's default)")
@click.option("--ollama-url", default="http://localhost:11434", help="Ollama base URL")
@click.option("--max-parallelism", default=8, type=int, help="Max parallel analyze_unit calls")
@click.option("--max-files", default=None, type=int, help="Cap number of source files analysed (useful for large repos)")
@click.option("--skip-tests/--include-tests", default=True, help="Skip test files (default: skip)")
@click.option("--analysis-passes", default=1, type=int, help="Completeness-refinement passes (re-analyse under-captured units)")
@click.option("--thread-id", default=None, help="Resume a previous run by thread ID")
@click.option("--langsmith-project", default=None, help="LangSmith project name for tracing")
@click.option("--no-cache", is_flag=True, default=False, help="Disable the on-disk LLM response cache for this run")
@click.option("--clear-cache", is_flag=True, default=False, help="Delete all cached LLM responses before running")
def main(repo: str, out: str, provider: str, model: str | None, ollama_url: str, max_parallelism: int, max_files: int | None, skip_tests: bool, analysis_passes: int, thread_id: str | None, langsmith_project: str | None, no_cache: bool, clear_cache: bool):
    """Ingest a codebase and produce a language-agnostic reimplementation spec."""
    from pipeline.model_catalog import provider_config, default_model

    provider = provider.lower()
    cfg = provider_config(provider)
    model = model or default_model(provider)
    os.environ["LLM_PROVIDER"] = provider
    os.environ["MODEL_ID"] = model
    os.environ["OLLAMA_BASE_URL"] = ollama_url

    # LLM response cache controls
    if no_cache:
        os.environ["LLM_CACHE"] = "0"
    if clear_cache:
        from pipeline.cache import clear
        removed = clear()
        print(f"Cleared LLM cache ({removed} entries)")
    key_env = cfg.get("api_key_env")
    if key_env and not os.environ.get(key_env):
        raise SystemExit(f"{key_env} is not set. Add it to .env or your environment.")

    # LangSmith tracing — enable if API key is set or project is specified
    if langsmith_project:
        os.environ["LANGCHAIN_PROJECT"] = langsmith_project
    if os.environ.get("LANGSMITH_API_KEY") or os.environ.get("LANGCHAIN_API_KEY"):
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGCHAIN_PROJECT", langsmith_project or "code-to-spec")
        print(f"LangSmith tracing enabled → project: {os.environ['LANGCHAIN_PROJECT']}")

    # Resolve a git URL to a local clone (no-op for local paths)
    from pipeline.repo_source import resolve_repo_source
    try:
        repo = resolve_repo_source(repo)
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(f"Could not resolve repository: {exc}")

    checkpointer = MemorySaver()
    graph = build_graph(checkpointer=checkpointer)

    tid = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}

    print(f"Thread ID: {tid}  (use --thread-id {tid} to resume)")
    print(f"Analyzing repo: {os.path.abspath(repo)}")

    print(f"Settings: max_files={max_files or 'all'}, skip_tests={skip_tests}, parallelism={max_parallelism}, analysis_passes={analysis_passes}")

    from pipeline.memory import RunMemory
    memory = RunMemory()
    prior_lessons = memory.get_past_context(os.path.abspath(repo))
    if prior_lessons:
        print("Loaded prior-run lessons (avoiding previously-flagged hallucinations)")

    initial_state = {
        "repo_path": os.path.abspath(repo),
        "output_path": os.path.abspath(out),
        "max_parallelism": max_parallelism,
        "max_files": max_files,
        "skip_tests": skip_tests,
        "max_analysis_passes": analysis_passes,
        "analysis_pass": 0,
        "revision_count": 0,
        "prior_lessons": prior_lessons,
        "unit_analyses": [],
        "map_errors": [],
        "behavioral_tests": [],
    }

    result = graph.invoke(initial_state, config=config)

    doc = result.get("final_document") or result.get("draft_document", "")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"Spec written to {out}")

    # Store this run's lessons + reflection for future runs of this repo
    hallucinations = result.get("review_findings", []) if not result.get("review_passed") else []
    try:
        from pipeline.reflection import reflect_on_run
        languages = result.get("languages_detected", [])
        unit_count = len(result.get("unit_analyses", []))
        reflection = reflect_on_run(os.path.basename(repo), languages, unit_count, hallucinations)
        memory.store_run(os.path.abspath(repo), model, languages, unit_count, hallucinations, reflection)
    except Exception:
        pass

    map_errors = result.get("map_errors", [])
    if map_errors:
        print(f"Warnings: {len(map_errors)} units failed analysis")
        for err in map_errors[:5]:
            print(f"  {err[:120]}")
        if len(map_errors) > 5:
            print(f"  ... and {len(map_errors) - 5} more errors")

    review_findings = result.get("review_findings", [])
    if result.get("review_passed"):
        print("Consistency review: PASSED (grounded in the analysis)")
    else:
        print(f"Consistency review: {len(review_findings)} finding(s)")
        for finding in review_findings[:3]:
            print(f"  - {finding}")
        if len(review_findings) > 3:
            print(f"  ... and {len(review_findings) - 3} more")

    if result.get("validation_passed"):
        print("Validation: PASSED")
    else:
        gaps = result.get("validation_gaps", [])
        if gaps:
            print(f"Validation: gaps found ({len(gaps)})")
            for gap in gaps[:3]:
                print(f"  - {gap}")


if __name__ == "__main__":
    main()
