"""
Index a completed run into the vector DB for RAG.

Stores three kinds of documents per repo collection:
  - source:     raw code of each analysed file (chunked) — for code questions
  - class_spec: the per-class spec markdown — for "what does X do" questions
  - spec:       the final reimplementation spec, by section — for spec questions
"""

from __future__ import annotations

import os

from pipeline.vectordb import collection_for, get_store


def _chunk(text: str, size: int = 1400, overlap: int = 150) -> list[str]:
    """Simple character chunker with overlap (no extra dependencies)."""
    text = text or ""
    if len(text) <= size:
        return [text] if text.strip() else []
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c.strip()]


def _split_spec_sections(spec: str) -> list[tuple[str, str]]:
    """Split the final spec on top-level (## / #) headings into (title, body)."""
    import re

    parts = re.split(r"(?m)^(#{1,2}\s+.*)$", spec)
    sections: list[tuple[str, str]] = []
    # parts = [pre, heading1, body1, heading2, body2, ...]
    if parts and parts[0].strip():
        sections.append(("Overview", parts[0].strip()))
    for i in range(1, len(parts), 2):
        title = parts[i].lstrip("# ").strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if body:
            sections.append((title, body))
    return sections or [("Spec", spec)]


def index_run(
    repo_path: str,
    class_docs: dict[str, str],
    spec_text: str,
    log=print,
) -> tuple[str, int]:
    """Embed and store this run's code + specs. Returns (collection, doc_count)."""
    from langchain_core.documents import Document

    collection = collection_for(repo_path)
    # Record which embeddings built this index so chat can match them later
    embed_provider = os.environ.get("EMBED_PROVIDER", os.environ.get("LLM_PROVIDER", "ollama")).lower()
    embed_model = (
        os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        if embed_provider == "openai"
        else os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    )
    store = get_store(collection, embed_meta={"embed_provider": embed_provider, "embed_model": embed_model})

    docs: list[Document] = []

    # 1. Per-unit spec markdown (keys are unit_ids; may be "<path>::<Class>")
    for unit_id, md in class_docs.items():
        for j, chunk in enumerate(_chunk(md)):
            docs.append(Document(
                page_content=chunk,
                metadata={"type": "class_spec", "path": unit_id, "chunk": j, "repo": repo_path},
            ))

    # 2. Raw source of each analysed file (dedupe the real paths behind split units)
    real_paths = {uid.split("::", 1)[0] for uid in class_docs}
    for path in real_paths:
        full = os.path.join(repo_path, path)
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
        except OSError:
            continue
        for j, chunk in enumerate(_chunk(source)):
            docs.append(Document(
                page_content=chunk,
                metadata={"type": "source", "path": path, "chunk": j, "repo": repo_path},
            ))

    # 3. Final spec, by section
    for title, body in _split_spec_sections(spec_text or ""):
        for j, chunk in enumerate(_chunk(body)):
            docs.append(Document(
                page_content=f"# {title}\n\n{chunk}",
                metadata={"type": "spec", "section": title, "chunk": j, "repo": repo_path},
            ))

    if not docs:
        return collection, 0

    log(f"Embedding and indexing {len(docs)} chunks into '{collection}'…")
    # Batch to keep memory and request sizes sane
    for i in range(0, len(docs), 64):
        store.add_documents(docs[i:i + 64])
    return collection, len(docs)
