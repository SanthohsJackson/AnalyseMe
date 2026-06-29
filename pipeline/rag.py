"""
Phase 7 — RAG retrieval for synthesis nodes.

On large codebases the synthesis nodes can't hold every module summary / test
in the prompt. `select_context` keeps the full set when it fits the budget
(best quality for small/medium repos) and otherwise switches to retrieval:
it passes a compact index of ALL items (for breadth) plus the full detail of
only the items most relevant to that node's task (for depth).

The index is an in-memory vector store using the same local Ollama embeddings
as the chat RAG, so it needs no database and adds embedding cost only when a
repo is actually large enough to need it.
"""

from __future__ import annotations

import os

# Character budget for a node's variable-size context block. Above this we
# switch from "send everything" to retrieval.
RAG_CHAR_BUDGET = int(os.environ.get("CTS_RAG_BUDGET", "12000"))


class RAGIndex:
    """Thin wrapper over an in-memory vector store of (id, text) records."""

    def __init__(self):
        from langchain_core.vectorstores import InMemoryVectorStore
        from pipeline.vectordb import get_embeddings

        self._vs = InMemoryVectorStore(embedding=get_embeddings())

    def add(self, items: list[tuple[str, str]]) -> None:
        from langchain_core.documents import Document

        self._vs.add_documents(
            [Document(page_content=text, metadata={"id": _id}) for _id, text in items if text]
        )

    def retrieve(self, query: str, k: int):
        return self._vs.similarity_search(query, k=k)


def select_context(
    full_text: str,
    records: list[dict],
    query: str,
    char_budget: int = RAG_CHAR_BUDGET,
    k: int = 12,
) -> tuple[str, bool]:
    """Return (context_text, used_rag).

    - When `full_text` fits the budget, return it unchanged (no embeddings,
      identical behaviour to before).
    - Otherwise build an index from `records` (each: {id, full, compact}),
      retrieve the top-k relevant items for `query`, and return a compact index
      of everything plus the full detail of the retrieved items.
    """
    if len(full_text) <= char_budget:
        return full_text, False

    try:
        index = RAGIndex()
        index.add([(r["id"], r["full"]) for r in records])
        hits = index.retrieve(query, k=min(k, len(records)))
        retrieved_ids = {h.metadata.get("id") for h in hits}
    except Exception:
        # Embeddings/store unavailable — degrade to a truncated compact view
        compact = "\n".join(r["compact"] for r in records)
        return compact[:char_budget], False

    compact_all = "\n".join(r["compact"] for r in records)
    detail = "\n\n".join(h.page_content for h in hits)
    text = (
        f"NOTE: this codebase is large ({len(records)} items); showing a compact index of all "
        f"items plus full detail for the {len(retrieved_ids)} most relevant to this task.\n\n"
        f"=== INDEX (all items, one line each) ===\n{compact_all}\n\n"
        f"=== DETAIL (most relevant items) ===\n{detail}"
    )
    return text, True
