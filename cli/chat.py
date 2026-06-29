"""
RAG chat REPL over a repo's indexed code + spec.

Retrieves the most relevant chunks from pgvector and asks the local LLM to
answer grounded in them, with source citations.
"""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule

console = Console()


def _format_context(docs) -> str:
    blocks = []
    for d in docs:
        meta = d.metadata or {}
        dtype = meta.get("type", "?")
        if dtype == "spec":
            label = f"SPEC §{meta.get('section', '?')}"
        elif dtype == "class_spec":
            label = f"CLASS SPEC {meta.get('path', '?')}"
        elif dtype == "source":
            label = f"SOURCE {meta.get('path', '?')}"
        else:
            label = dtype
        blocks.append(f"[{label}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)


def _sources_line(docs) -> str:
    seen, out = set(), []
    for d in docs:
        meta = d.metadata or {}
        key = meta.get("section") or meta.get("path") or meta.get("type")
        tag = f"{meta.get('type', '?')}:{key}"
        if tag not in seen:
            seen.add(tag)
            out.append(tag)
    return ", ".join(out)


def chat_repl(collection: str, k: int = 8) -> None:
    """Interactive Q&A loop against an indexed collection."""
    from pipeline.vectordb import get_store, check_connection
    from pipeline.prompts.prompts import CHAT_PROMPT
    from pipeline.llm import call_llm_text, get_provider, get_model_id

    import os as _os
    console.print(
        f"[dim]chat model: {get_provider()} / {get_model_id()}  ·  "
        f"embeddings: {_os.environ.get('EMBED_PROVIDER', _os.environ.get('LLM_PROVIDER','ollama'))}[/dim]"
    )

    ok, msg = check_connection()
    if not ok:
        console.print(f"[red]{msg}[/red]")
        return

    try:
        store = get_store(collection)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Could not open collection '{collection}': {exc}[/red]")
        return

    console.print(Panel(
        f"[bold cyan]Chat about: {collection}[/bold cyan]\n"
        "[dim]Ask about the code or the generated spec. Type 'exit' or Ctrl-D to quit.[/dim]",
        border_style="cyan",
    ))

    while True:
        try:
            question = console.input("\n[bold green]you ›[/bold green] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            return
        if not question:
            continue
        if question.lower() in {"exit", "quit", ":q"}:
            return

        try:
            docs = store.similarity_search(question, k=k)
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Retrieval failed: {exc}[/red]")
            continue

        if not docs:
            console.print("[yellow]No indexed content matched that question.[/yellow]")
            continue

        with console.status("[dim]thinking…[/dim]"):
            answer = call_llm_text(CHAT_PROMPT.format(
                context=_format_context(docs)[:18000],
                question=question,
            ))

        console.print(Rule(style="dim"))
        console.print(Markdown(answer))
        console.print(f"[dim]sources: {_sources_line(docs)}[/dim]")
