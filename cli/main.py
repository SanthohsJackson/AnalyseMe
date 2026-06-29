"""
Rich terminal UI for the Analyse Me pipeline.
Modelled on TradingAgents CLI (cli/main.py).
"""

import datetime
import os
import time
import uuid
from collections import deque
from pathlib import Path

import questionary
import typer
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from cli.utils import (
    ask_analysis_passes,
    ask_max_files,
    ask_model,
    ask_output_file,
    ask_provider,
    ask_repo_path,
    ask_skip_tests,
)

console = Console()

app = typer.Typer(
    name="analyse-me",
    help="Analyse Me: Generate language-agnostic reimplementation specs from any codebase",
)


@app.callback(invoke_without_command=True)
def _default(ctx: typer.Context) -> None:
    """Drop into the startup menu when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        menu()

# Single source of truth for pipeline stages: (display label, node id)
STAGES: list[tuple[str, str]] = [
    ("Ingestion",          "ingest"),
    ("Routing",            "route_units"),
    ("Unit Analysis",      "analyze_unit"),
    ("Completeness",       "review_completeness"),
    ("Module Reduction",   "reduce_modules"),
    ("System Synthesis",   "synthesize_system"),
    ("Architecture",       "extract_architecture"),
    ("Test Generation",    "generate_tests"),
    ("Diagram",            "generate_diagram"),
    ("Assembly",           "assemble_document"),
    ("Review",             "review_consistency"),
    ("Validation",         "validate"),
]

NODE_IDS = [node_id for _, node_id in STAGES]
NODE_LABEL = {node_id: label for label, node_id in STAGES}


class PipelineBuffer:
    """Mutable state shared between the stream loop and the display renderer."""

    def __init__(self, max_messages: int = 100):
        self.messages: deque = deque(maxlen=max_messages)
        self.node_status: dict[str, str] = {node_id: "pending" for node_id in NODE_IDS}
        self.current_node: str | None = None
        self.current_output: str | None = None   # most recent draft / section for preview
        self.stats: dict = {
            "files": 0,
            "units_done": 0,
            "units_total": 0,
            "llm_calls": 0,
            "errors": 0,
            "review_findings": 0,
        }
        self.start_time: float | None = None

        # Persisted artifacts for the interactive viewer
        self.stage_docs: dict[str, str] = {}     # node_id -> markdown
        self.class_docs: dict[str, str] = {}     # unit path -> markdown spec
        self.review_findings: list[str] = []
        self.review_passed: bool | None = None
        self.artifacts_dir: Path | None = None
        self.languages: list[str] = []           # captured for cross-run memory

    def add_message(self, msg_type: str, content: str) -> None:
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.messages.append((ts, msg_type, content))

    def set_node(self, node_id: str, status: str) -> None:
        if node_id in self.node_status:
            self.node_status[node_id] = status
            if status == "in_progress":
                self.current_node = node_id

    def complete_node(self, node_id: str) -> None:
        self.set_node(node_id, "completed")


buffer = PipelineBuffer()


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    # Progress occupies the full-height left column so all 10 stages always fit;
    # the right column stacks the log over the spec/output preview.
    layout["main"].split_row(
        Layout(name="progress", minimum_size=30, ratio=2),
        Layout(name="right", ratio=5),
    )
    layout["right"].split_column(
        Layout(name="messages", ratio=2),
        Layout(name="output", ratio=3),
    )
    return layout


def update_display(layout: Layout) -> None:
    # ── Header ────────────────────────────────────────────────────────────────
    layout["header"].update(Panel(
        "[bold cyan]Analyse Me[/bold cyan]  "
        "[dim]Generate language-agnostic reimplementation specs[/dim]",
        border_style="cyan",
        padding=(0, 2),
    ))

    # ── Progress table ─────────────────────────────────────────────────────────
    tbl = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAD,
        padding=(0, 1),
        expand=True,
    )
    tbl.add_column("Stage", style="cyan", justify="left", ratio=2)
    tbl.add_column("Status", style="yellow", justify="center", ratio=1)

    for label, node_id in STAGES:
        status = buffer.node_status.get(node_id, "pending")
        if status == "in_progress":
            status_cell = Spinner("dots", text="[blue]running[/blue]")
        else:
            color = {"pending": "yellow", "completed": "green", "error": "red"}.get(status, "white")
            status_cell = f"[{color}]{status}[/{color}]"
        tbl.add_row(label, status_cell)

    layout["progress"].update(Panel(
        tbl,
        title="Pipeline Progress",
        border_style="cyan",
        padding=(0, 1),
    ))

    # ── Messages panel ─────────────────────────────────────────────────────────
    msg_tbl = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.MINIMAL,
        show_lines=True,
        padding=(0, 1),
        expand=True,
    )
    msg_tbl.add_column("Time",    style="cyan",  width=8,  justify="center")
    msg_tbl.add_column("Type",    style="green", width=8,  justify="center")
    msg_tbl.add_column("Content", style="white", ratio=1)

    recent = list(buffer.messages)[-12:][::-1]
    for ts, mtype, content in recent:
        msg_tbl.add_row(ts, mtype, Text(content[:200], overflow="fold"))

    layout["messages"].update(Panel(
        msg_tbl,
        title="Log",
        border_style="blue",
        padding=(1, 1),
    ))

    # ── Output panel ───────────────────────────────────────────────────────────
    # While the reviewer is running or has flagged findings, the panel shows the
    # anti-hallucination report; otherwise it shows the live spec preview.
    reviewing = buffer.current_node == "review_consistency"
    show_review = reviewing or buffer.review_passed is False

    if show_review:
        if buffer.review_passed is None:
            output_renderable = Markdown(
                "### Consistency Review — running…\n\n"
                "_Grounding the draft against the extracted interfaces and "
                "dependencies to catch invented architecture._"
            )
            output_title = "Review (running)"
            border = "yellow"
        elif buffer.review_passed:
            output_renderable = Markdown("### Consistency Review: PASSED ✓\n\nNo hallucinations found.")
            output_title = "Review — PASSED"
            border = "green"
        else:
            findings_md = "\n".join(f"{i}. {f}" for i, f in enumerate(buffer.review_findings, 1))
            output_renderable = Markdown(
                f"### ⚠ Consistency Review — {len(buffer.review_findings)} unsupported claim(s)\n\n"
                f"_These appear in the draft but are not backed by the analysis "
                f"(likely hallucinations). The pipeline will try to correct them._\n\n"
                f"{findings_md}"
            )
            output_title = "Review — HALLUCINATIONS FLAGGED"
            border = "red"
    elif buffer.current_output:
        output_renderable = Markdown(buffer.current_output[:3000])
        output_title = "Spec Preview"
        border = "green"
    else:
        node_label = NODE_LABEL.get(buffer.current_node or "", buffer.current_node or "...")
        output_renderable = (
            f"[italic dim]Waiting for output... (current stage: {node_label})[/italic dim]"
        )
        output_title = "Output"
        border = "green"

    layout["output"].update(Panel(
        output_renderable,
        title=output_title,
        border_style=border,
        padding=(1, 2),
    ))

    # ── Footer stats ───────────────────────────────────────────────────────────
    elapsed = ""
    if buffer.start_time:
        s = int(time.time() - buffer.start_time)
        elapsed = f"⏱ {s // 60:02d}:{s % 60:02d}"

    st = buffer.stats
    review_str = ""
    if buffer.review_passed is True:
        review_str = "Review: [green]grounded ✓[/green]"
    elif buffer.review_passed is False:
        review_str = f"Review: [red]{st['review_findings']} flags ✗[/red]"
    parts = [
        f"Files: {st['files']}",
        f"Units: {st['units_done']}/{st['units_total']}",
        f"LLM calls: {st['llm_calls']}",
        f"Errors: {st['errors']}",
        review_str,
        elapsed,
    ]
    footer_tbl = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    footer_tbl.add_column("s", justify="center")
    footer_tbl.add_row(" | ".join(p for p in parts if p))
    layout["footer"].update(Panel(footer_tbl, border_style="grey50"))


# ---------------------------------------------------------------------------
# User wizard
# ---------------------------------------------------------------------------

def get_user_selections() -> dict:
    """Interactive wizard — collect all settings before starting the pipeline."""
    welcome_path = Path(__file__).parent / "static" / "welcome.txt"
    banner = welcome_path.read_text() if welcome_path.exists() else "Analyse Me"

    console.print(Align.center(Panel(
        f"[bold cyan]{banner}[/bold cyan]\n"
        "[bold]Analyse any codebase — produce a language-agnostic reimplementation spec[/bold]\n\n"
        "[dim]Powered by LangGraph + Ollama / OpenAI[/dim]",
        border_style="cyan",
        padding=(1, 4),
        title="Analyse Me",
        subtitle="LangGraph Pipeline",
    )))
    console.print()

    def step_box(title: str, hint: str) -> None:
        console.print(Panel(
            f"[bold]{title}[/bold]\n[dim]{hint}[/dim]",
            border_style="blue",
            padding=(1, 2),
        ))

    step_box("Step 1: Repository", "Choose the codebase you want to analyse")
    repo_path = ask_repo_path()

    step_box("Step 2: Output File", "Where to write the generated spec")
    out_file = ask_output_file()

    step_box("Step 3: LLM Provider", "Local Ollama or a hosted provider (OpenAI, DeepSeek, …)")
    provider = ask_provider()
    step_box("Step 3b: Model", f"Select the model to use for {provider}")
    model = ask_model(provider)

    step_box("Step 4: File Cap", "Limit files to analyse (recommended for large repos)")
    max_files = ask_max_files()

    step_box("Step 5: Test Files", "Whether to include test files in the analysis")
    skip_tests = ask_skip_tests()

    step_box("Step 6: Analysis Passes",
             "How many times to re-analyse under-captured units to fill gaps")
    analysis_passes = ask_analysis_passes()

    return {
        "repo_path": repo_path,
        "out_file":  out_file,
        "provider":  provider,
        "model":     model,
        "max_files": max_files,
        "skip_tests": skip_tests,
        "analysis_passes": analysis_passes,
    }


# ---------------------------------------------------------------------------
# Artifact persistence (per-stage docs + per-class specs)
# ---------------------------------------------------------------------------

def _safe_name(path: str) -> str:
    """Turn a unit path into a safe filename."""
    return path.replace("/", "__").replace("\\", "__").replace(":", "_") + ".md"


def _persist_class_spec(ua) -> None:
    """Render and store the per-class spec, both in the buffer and on disk.

    Keyed by unit_id (unique) since a split large file yields several units that
    share one path.
    """
    from pipeline.artifacts import render_class_spec, write_text

    md = render_class_spec(ua)
    buffer.class_docs[ua.unit_id] = md
    if buffer.artifacts_dir:
        write_text(buffer.artifacts_dir / "classes" / _safe_name(ua.unit_id), md)


def _persist_stage_doc(node_id: str, update: dict) -> None:
    """Render and store a per-stage doc, both in the buffer and on disk."""
    from pipeline.artifacts import render_stage_doc, write_text

    md = render_stage_doc(node_id, update)
    if not md:
        return
    buffer.stage_docs[node_id] = md
    if buffer.artifacts_dir:
        idx = NODE_IDS.index(node_id) if node_id in NODE_IDS else 99
        write_text(buffer.artifacts_dir / "stages" / f"{idx:02d}_{node_id}.md", md)


# ---------------------------------------------------------------------------
# Interactive viewer (post-run)
# ---------------------------------------------------------------------------

def _pause(message: str = "Press Enter to return to the menu…") -> None:
    """Robust pause that works across terminals/questionary versions."""
    try:
        input(f"\n{message} ")
    except (EOFError, KeyboardInterrupt):
        pass


def _render_doc(title: str, content: str) -> None:
    """Clear the screen, render a markdown doc, then wait so it stays readable
    until the user chooses to go back. Avoids the fragile system pager."""
    console.clear()
    console.print(Rule(title, style="bold cyan"))
    console.print()
    console.print(Markdown(content or "_(empty)_"))
    console.print()
    console.print(Rule(style="dim"))
    _pause()


def interactive_viewer(final_doc: str) -> None:
    """Let the user browse stages, per-class specs, the review report, and the spec."""
    while True:
        choices = [questionary.Choice("📄 Final spec document", value=("final", None))]

        # Stage docs in pipeline order
        for label, node_id in STAGES:
            if node_id in buffer.stage_docs:
                choices.append(questionary.Choice(f"  Stage: {label}", value=("stage", node_id)))

        # Review report shortcut
        if buffer.review_passed is not None:
            mark = "✓" if buffer.review_passed else f"✗ {len(buffer.review_findings)} flags"
            choices.append(questionary.Choice(f"🔍 Review report  [{mark}]", value=("review", None)))

        # Per-class specs
        for path in sorted(buffer.class_docs):
            choices.append(questionary.Choice(f"  Class: {path}", value=("class", path)))

        choices.append(questionary.Choice("✖ Exit viewer", value=("exit", None)))

        console.print()
        console.print(Rule("Document Viewer  (↑/↓ to move, Enter to open)", style="bold green"))
        try:
            answer = questionary.select(
                "View which document?",
                choices=choices,
                style=questionary.Style([
                    ("selected", "fg:cyan noinherit"),
                    ("highlighted", "fg:cyan noinherit"),
                ]),
            ).ask()
        except Exception as exc:
            console.print(f"[red]Viewer menu error: {exc}[/red]")
            return

        if answer is None:
            return
        kind, key = answer

        if kind == "exit":
            return
        elif kind == "final":
            _render_doc("Final Spec Document", final_doc or "_(empty)_")
        elif kind == "stage":
            _render_doc(f"Stage: {NODE_LABEL.get(key, key)}", buffer.stage_docs.get(key, "_(none)_"))
        elif kind == "class":
            _render_doc(f"Class Spec: {key}", buffer.class_docs.get(key, "_(none)_"))
        elif kind == "review":
            if buffer.review_passed:
                body = "**PASSED** — the document is grounded in the analysis; no hallucinations found."
            else:
                body = "**FINDINGS** — unsupported claims detected:\n\n" + "\n".join(
                    f"- {f}" for f in buffer.review_findings
                )
            _render_doc("Consistency Review (anti-hallucination)", body)


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(no_cache: bool = False, clear_cache: bool = False) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Load .env from project root
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    # LLM cache controls (after .env so LLM_CACHE_DIR is honoured)
    if no_cache:
        os.environ["LLM_CACHE"] = "0"
    if clear_cache:
        from pipeline.cache import clear
        console.print(f"[dim]Cleared LLM cache ({clear()} entries)[/dim]")

    selections = get_user_selections()

    # Resolve a git URL to a local clone (no-op for local paths)
    from pipeline.repo_source import resolve_repo_source
    try:
        selections["repo_path"] = resolve_repo_source(
            selections["repo_path"],
            log=lambda m: console.print(f"[dim]{m}[/dim]"),
        )
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Could not resolve repository: {exc}[/red]")
        return

    from pipeline.model_catalog import provider_config

    provider = selections.get("provider", "ollama")
    os.environ["LLM_PROVIDER"] = provider
    os.environ["MODEL_ID"] = selections["model"]
    cfg = provider_config(provider)
    key_env = cfg.get("api_key_env")
    if key_env and not os.environ.get(key_env):
        console.print(f"[red]{key_env} is not set. Add it to .env or your shell and re-run.[/red]")
        return

    # LangSmith tracing
    if os.environ.get("LANGSMITH_API_KEY") or os.environ.get("LANGCHAIN_API_KEY"):
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGCHAIN_PROJECT", "code-to-spec")
        console.print(
            f"[dim]LangSmith tracing → project: {os.environ['LANGCHAIN_PROJECT']}[/dim]"
        )

    from graph import build_graph
    from langgraph.checkpoint.memory import MemorySaver

    checkpointer = MemorySaver()
    graph = build_graph(checkpointer=checkpointer)

    tid = str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}
    console.print(f"[dim]Thread ID: {tid}[/dim]")

    # Artifacts dir: <out_stem>_artifacts/ next to the spec file
    out_path = Path(selections["out_file"]).resolve()
    artifacts_dir = out_path.parent / f"{out_path.stem}_artifacts"
    (artifacts_dir / "stages").mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "classes").mkdir(parents=True, exist_ok=True)
    buffer.artifacts_dir = artifacts_dir
    console.print(f"[dim]Artifacts → {artifacts_dir}[/dim]")

    # Cross-run memory: inject lessons (hallucinations caught) from prior runs of this repo
    from pipeline.memory import RunMemory
    memory = RunMemory()
    prior_lessons = memory.get_past_context(selections["repo_path"])
    if prior_lessons:
        console.print("[dim]Loaded prior-run lessons (avoiding previously-flagged hallucinations)[/dim]")

    initial_state = {
        "repo_path":       selections["repo_path"],
        "output_path":     str(out_path),
        "artifacts_dir":   str(artifacts_dir),
        "max_parallelism": 8,
        "max_files":       selections["max_files"],
        "skip_tests":      selections["skip_tests"],
        "max_analysis_passes": selections["analysis_passes"],
        "analysis_pass":   0,
        "revision_count":  0,
        "prior_lessons":   prior_lessons,
        "unit_analyses":   [],
        "map_errors":      [],
        "behavioral_tests": [],
    }

    buffer.start_time = time.time()
    buffer.add_message("System", f"Repo: {selections['repo_path']}")
    buffer.add_message("System", f"Model: {selections['model']}")

    layout = create_layout()
    completed_nodes: set[str] = set()

    with Live(layout, refresh_per_second=4) as _live:
        update_display(layout)

        try:
            # stream_mode="updates" yields {node_name: state_update_dict} per step
            for chunk in graph.stream(initial_state, config=config, stream_mode="updates"):
                for node_name, update in chunk.items():
                    # Mark the node in-progress, complete the previous one
                    if node_name in NODE_IDS and node_name not in completed_nodes:
                        if buffer.current_node and buffer.current_node != node_name:
                            buffer.complete_node(buffer.current_node)
                            completed_nodes.add(buffer.current_node)
                        buffer.set_node(node_name, "in_progress")

                    if not isinstance(update, dict):
                        update_display(layout)
                        continue

                    # ── Inspect the state update fields ───────────────────────
                    files = update.get("files")
                    if files is not None:
                        buffer.stats["files"] = len(files)
                        buffer.add_message("Ingest", f"{len(files)} files found")

                    langs = update.get("languages_detected")
                    if langs:
                        buffer.languages = list(langs)

                    units = update.get("units_to_analyze")
                    if units is not None:
                        buffer.stats["units_total"] = len(units)
                        buffer.add_message("Route", f"{len(units)} units queued")

                    analyses = update.get("unit_analyses")
                    if analyses:
                        buffer.stats["units_done"] += len(analyses)
                        buffer.stats["llm_calls"] += len(analyses)
                        last_path = getattr(analyses[-1], "path", str(analyses[-1]))
                        buffer.add_message("Analyse", f"✓ {last_path}")
                        # Persist a per-class spec for each analysed unit
                        for ua in analyses:
                            _persist_class_spec(ua)

                    errors = update.get("map_errors")
                    if errors:
                        buffer.stats["errors"] += len(errors)
                        for err in errors:
                            buffer.add_message("Error", str(err)[:120])

                    # Completeness review / multi-pass refinement
                    if "analysis_complete" in update:
                        questions = update.get("analysis_questions", {}) or {}
                        n_gaps = sum(len(v) for v in questions.values())
                        ap = update.get("analysis_pass", 0)
                        buffer.stats["llm_calls"] += 1
                        if update.get("analysis_complete"):
                            buffer.add_message("Complete", f"pass {ap}: all units fully captured ✓")
                        else:
                            buffer.add_message(
                                "Complete",
                                f"pass {ap}: {n_gaps} gap(s) across {len(questions)} unit(s) — refining",
                            )
                            for uid, qs in list(questions.items())[:5]:
                                buffer.add_message("Gap?", f"{uid}: {qs[0][:90]}" if qs else uid)

                    summaries = update.get("module_summaries")
                    if summaries:
                        buffer.add_message("Reduce", f"{len(summaries)} modules summarised")

                    overview = update.get("system_overview")
                    if overview:
                        buffer.stats["llm_calls"] += 1
                        buffer.add_message("Synthesis", "System overview generated")
                        buffer.current_output = f"## System Overview\n\n{overview}"

                    schemas = update.get("data_schemas")
                    if schemas:
                        buffer.add_message("Arch", f"{len(schemas)} data schemas extracted")

                    tests = update.get("behavioral_tests")
                    if tests:
                        buffer.add_message("Tests", f"{len(tests)} acceptance tests generated")

                    diagram = update.get("architecture_diagram")
                    if diagram:
                        edge_count = diagram.count("-->")
                        buffer.add_message("Diagram", f"architecture diagram built ({edge_count} edges)")
                        buffer.current_output = diagram

                    draft = update.get("draft_document")
                    if draft:
                        buffer.stats["llm_calls"] += 1
                        buffer.add_message("Assembly", "Draft spec assembled")
                        buffer.current_output = draft

                    # Anti-hallucination review results
                    rev_passed = update.get("review_passed")
                    if rev_passed is not None:
                        buffer.review_passed = rev_passed
                        findings = update.get("review_findings", []) or []
                        buffer.review_findings = findings
                        buffer.stats["review_findings"] = len(findings)
                        buffer.stats["llm_calls"] += 1
                        if rev_passed:
                            buffer.add_message("Review", "grounded ✓ no hallucinations")
                        else:
                            buffer.add_message("Review", f"{len(findings)} unsupported claim(s) flagged")
                            for f in findings[:5]:
                                buffer.add_message("Flag", str(f)[:120])

                    val_passed = update.get("validation_passed")
                    if val_passed is not None:
                        buffer.add_message("Validate", "PASSED" if val_passed else "gaps found")

                    gaps = update.get("validation_gaps")
                    if gaps:
                        for gap in gaps:
                            buffer.add_message("Gap", str(gap)[:120])

                    final = update.get("final_document")
                    if final:
                        buffer.current_output = final
                        buffer.add_message("Done", "Final spec ready")

                    # Capture + persist a per-stage doc for this update
                    if node_name in NODE_IDS:
                        _persist_stage_doc(node_name, update)

                update_display(layout)

        except Exception as exc:
            buffer.add_message("Error", str(exc))
            update_display(layout)
            raise

        # Mark any remaining nodes as completed
        for node_id in NODE_IDS:
            buffer.complete_node(node_id)
        update_display(layout)

    # ── Write output ───────────────────────────────────────────────────────────
    out_path = Path(selections["out_file"])
    doc = buffer.current_output or ""
    # Atomic write so an interrupted write never leaves a corrupt spec
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(doc, encoding="utf-8")
    tmp.replace(out_path)

    # Store this run in cross-run memory (lessons for next time) + a terse reflection
    try:
        from pipeline.reflection import reflect_on_run
        reflection = reflect_on_run(
            repo_name=Path(selections["repo_path"]).name,
            languages=buffer.languages,
            unit_count=buffer.stats["units_done"],
            hallucinations=buffer.review_findings,
        )
        memory.store_run(
            repo_path=selections["repo_path"],
            model=selections["model"],
            languages=buffer.languages,
            unit_count=buffer.stats["units_done"],
            hallucinations=buffer.review_findings,
            reflection=reflection,
        )
    except Exception:
        pass  # memory is best-effort

    elapsed = int(time.time() - buffer.start_time)
    console.print(
        f"\n[bold green]Done![/bold green] Spec written to "
        f"[cyan]{out_path.resolve()}[/cyan]  "
        f"({elapsed // 60:02d}:{elapsed % 60:02d})"
    )

    if buffer.stats["errors"]:
        console.print(
            f"[yellow]{buffer.stats['errors']} unit(s) failed analysis — check log above[/yellow]"
        )

    # Review verdict summary
    if buffer.review_passed is True:
        console.print("[green]Consistency review: PASSED — spec is grounded in the analysis.[/green]")
    elif buffer.review_passed is False:
        console.print(
            f"[red]Consistency review: {len(buffer.review_findings)} unsupported claim(s) flagged "
            f"(possible hallucinations).[/red]"
        )

    console.print(
        f"[dim]Stage docs: {buffer.artifacts_dir / 'stages'}\n"
        f"Class specs: {buffer.artifacts_dir / 'classes'}[/dim]"
    )

    # Interactive viewer: browse stages, class specs, review, and final spec
    open_viewer = typer.prompt("\nOpen interactive document viewer?", default="Y").strip().upper()
    if open_viewer in ("Y", "YES", ""):
        interactive_viewer(doc)

    # RAG: index code + spec into the vector DB and offer a chat session
    do_index = typer.prompt(
        "\nIndex this run into the vector DB for chat?", default="Y"
    ).strip().upper()
    if do_index in ("Y", "YES", ""):
        from pipeline.vectordb import check_connection, collection_for
        ok, msg = check_connection()
        if not ok:
            console.print(f"[yellow]{msg}[/yellow]")
        else:
            try:
                from pipeline.indexer import index_run
                collection, n = index_run(
                    selections["repo_path"], buffer.class_docs, doc,
                    log=lambda m: console.print(f"[dim]{m}[/dim]"),
                )
                console.print(f"[green]Indexed {n} chunks into '{collection}'.[/green]")
                start_chat = typer.prompt("Start chat now?", default="Y").strip().upper()
                if start_chat in ("Y", "YES", ""):
                    from cli.chat import chat_repl

                    # Pin embeddings to the provider that built this index (must match)
                    os.environ.setdefault("EMBED_PROVIDER", os.environ.get("LLM_PROVIDER", "ollama"))

                    # Offer to chat with a different (e.g. stronger) model than the run used
                    keep = typer.prompt(
                        f"Chat using {provider}/{selections['model']}? (n to pick another)",
                        default="Y",
                    ).strip().upper()
                    if keep in ("N", "NO"):
                        from pipeline.model_catalog import provider_config
                        chat_provider = ask_provider()
                        chat_model = ask_model(chat_provider)
                        cfg = provider_config(chat_provider)
                        key_env = cfg.get("api_key_env")
                        if key_env and not os.environ.get(key_env):
                            console.print(f"[yellow]{key_env} not set — falling back to {provider}.[/yellow]")
                        else:
                            os.environ["LLM_PROVIDER"] = chat_provider
                            os.environ["MODEL_ID"] = chat_model

                    chat_repl(collection)
            except Exception as exc:  # noqa: BLE001
                console.print(f"[red]Indexing failed: {exc}[/red]")


# ---------------------------------------------------------------------------
# Typer commands
# ---------------------------------------------------------------------------

_NO_CACHE_OPT = typer.Option(False, "--no-cache", help="Disable the on-disk LLM response cache for this run")
_CLEAR_CACHE_OPT = typer.Option(False, "--clear-cache", help="Delete all cached LLM responses before running")


@app.command()
def analyse(no_cache: bool = _NO_CACHE_OPT, clear_cache: bool = _CLEAR_CACHE_OPT) -> None:
    """Interactive wizard + live pipeline display."""
    run_pipeline(no_cache=no_cache, clear_cache=clear_cache)


# Alias so both spellings work
@app.command(hidden=True)
def analyze(no_cache: bool = _NO_CACHE_OPT, clear_cache: bool = _CLEAR_CACHE_OPT) -> None:
    """Alias for analyse."""
    run_pipeline(no_cache=no_cache, clear_cache=clear_cache)


@app.command(name="clear-cache")
def clear_cache_cmd() -> None:
    """Delete all cached LLM responses."""
    _load_env()
    from pipeline.cache import clear
    console.print(f"[green]Cleared {clear()} cached LLM response(s)[/green]")


def _load_env() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def run_chat(repo: str | None = None, provider: str | None = None,
             model: str | None = None, interactive_model: bool = False) -> None:
    """Open a RAG chat over a previously-indexed codebase + spec."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    _load_env()

    from pipeline.vectordb import (
        check_connection, collection_for, list_collections, collection_embed_config,
    )
    from pipeline.model_catalog import provider_config, default_model
    from cli.chat import chat_repl

    ok, msg = check_connection()
    if not ok:
        console.print(f"[red]{msg}[/red]")
        return

    # Optionally let the user pick the chat model interactively
    if interactive_model and not provider:
        from pipeline.llm import get_model_id, get_provider
        keep = typer.prompt(
            f"Chat using {get_provider()}/{get_model_id()}? (n to pick another)", default="Y"
        ).strip().upper()
        if keep in ("N", "NO"):
            provider = ask_provider()
            model = ask_model(provider)

    if provider:
        cfg = provider_config(provider)
        os.environ["LLM_PROVIDER"] = provider
        os.environ["MODEL_ID"] = model or default_model(provider)
        key_env = cfg.get("api_key_env")
        if key_env and not os.environ.get(key_env):
            console.print(f"[red]{key_env} is not set.[/red]")
            return
    elif model:
        os.environ["MODEL_ID"] = model

    # Resolve the collection: explicit repo, else pick from indexed ones
    if repo:
        from pipeline.repo_source import resolve_repo_source
        try:
            repo_path = resolve_repo_source(repo, log=lambda m: console.print(f"[dim]{m}[/dim]"))
        except (ValueError, RuntimeError) as exc:
            console.print(f"[red]{exc}[/red]")
            return
        collection = collection_for(repo_path)
    else:
        collections = list_collections()
        if not collections:
            console.print("[yellow]No indexed codebases yet. Run 'analyse' and index a run first.[/yellow]")
            return
        collection = questionary.select("Chat about which indexed codebase?", choices=collections).ask()
        if not collection:
            return

    # CRITICAL: embeddings must match what built this index. Auto-detect and apply.
    embed = collection_embed_config(collection)
    if embed:
        os.environ["EMBED_PROVIDER"] = embed["provider"]
        if embed.get("model"):
            key = "OPENAI_EMBED_MODEL" if embed["provider"] == "openai" else "OLLAMA_EMBED_MODEL"
            os.environ[key] = embed["model"]
        if embed["provider"] == "openai" and not os.environ.get("OPENAI_API_KEY"):
            console.print("[red]This index uses OpenAI embeddings but OPENAI_API_KEY is not set.[/red]")
            return
        console.print(f"[dim]embeddings: {embed['provider']} / {embed.get('model','?')} (matched to index)[/dim]")
    else:
        os.environ.setdefault("EMBED_PROVIDER", os.environ.get("LLM_PROVIDER", "ollama"))

    chat_repl(collection)


@app.command()
def chat(
    repo: str = typer.Option(None, help="Repo path/URL whose index to chat with"),
    provider: str = typer.Option(None, help="Chat LLM provider (e.g. openai); defaults to .env LLM_PROVIDER"),
    model: str = typer.Option(None, help="Chat model id (defaults to the provider's default)"),
) -> None:
    """Chat (RAG) about a previously-indexed codebase + spec."""
    run_chat(repo=repo, provider=provider, model=model)


@app.command()
def menu() -> None:
    """Startup menu — choose to analyse a codebase or chat about an existing spec."""
    _load_env()
    welcome_path = Path(__file__).parent / "static" / "welcome.txt"
    if welcome_path.exists():
        console.print(f"[bold cyan]{welcome_path.read_text()}[/bold cyan]")

    choice = questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice("Analyse a codebase (generate a new spec)", value="analyse"),
            questionary.Choice("Chat about an existing indexed spec", value="chat"),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
        ]),
    ).ask()

    if choice == "analyse":
        run_pipeline()
    elif choice == "chat":
        run_chat(interactive_model=True)


if __name__ == "__main__":
    app()
