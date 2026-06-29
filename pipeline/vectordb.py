"""
pgvector-backed vector store for RAG over the codebase and generated spec.

Uses langchain_postgres.PGVector + Ollama embeddings (nomic-embed-text by
default — fully local). Each repo gets its own collection so chat is scoped to
one codebase.
"""

from __future__ import annotations

import hashlib
import os
import re

DEFAULT_CONN = "postgresql+psycopg://cts:cts@localhost:5433/cts"


def get_conn_string() -> str:
    return os.environ.get("POSTGRES_CONN", DEFAULT_CONN)


def get_embeddings():
    """Embeddings for RAG.

    OpenAI uses its own embeddings; every other provider (Ollama and the various
    OpenAI-compatible chat providers that don't expose embeddings) falls back to
    local Ollama `nomic-embed-text`. Override with EMBED_PROVIDER if needed.
    """
    embed_provider = os.environ.get(
        "EMBED_PROVIDER", os.environ.get("LLM_PROVIDER", "ollama")
    ).strip().lower()

    if embed_provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        kwargs = {"model": os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-small")}
        if os.environ.get("OPENAI_BASE_URL"):
            kwargs["base_url"] = os.environ["OPENAI_BASE_URL"]
        return OpenAIEmbeddings(**kwargs)

    from langchain_ollama import OllamaEmbeddings

    return OllamaEmbeddings(
        model=os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


def collection_for(repo_path: str) -> str:
    """Stable, unique collection name for a repo (basename + path hash)."""
    base = os.path.basename(os.path.normpath(repo_path)) or "repo"
    base = re.sub(r"[^a-zA-Z0-9_]", "_", base)
    h = hashlib.sha1(repo_path.encode()).hexdigest()[:8]
    return f"cts_{base}_{h}"


def get_store(collection: str, embed_meta: dict | None = None):
    """Return a PGVector store for the given collection (creates it if needed).

    embed_meta (e.g. {"embed_provider": "openai", "embed_model": "..."}) is
    stored on the collection so chat can later pick matching embeddings.
    """
    from langchain_postgres import PGVector

    kwargs = dict(
        embeddings=get_embeddings(),
        collection_name=collection,
        connection=get_conn_string(),
        use_jsonb=True,
    )
    if embed_meta:
        kwargs["collection_metadata"] = embed_meta
    return PGVector(**kwargs)


def _provider_from_dim(dim: int) -> dict | None:
    """Map an embedding dimension to a likely provider/model."""
    return {
        768: {"provider": "ollama", "model": "nomic-embed-text"},
        1024: {"provider": "ollama", "model": "mxbai-embed-large"},
        1536: {"provider": "openai", "model": "text-embedding-3-small"},
        3072: {"provider": "openai", "model": "text-embedding-3-large"},
    }.get(dim)


def collection_embed_config(collection: str) -> dict | None:
    """Determine which embeddings a collection was built with.

    Prefers metadata stored at index time; falls back to detecting the stored
    vector dimension. Returns {"provider", "model"} or None.
    """
    try:
        import psycopg

        with psycopg.connect(_raw_conn_string(), connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT cmetadata FROM langchain_pg_collection WHERE name = %s", (collection,)
                )
                row = cur.fetchone()
                meta = row[0] if row else None
                if isinstance(meta, dict) and meta.get("embed_provider"):
                    return {"provider": meta["embed_provider"], "model": meta.get("embed_model")}

                # Fallback: detect from the stored vector dimension
                cur.execute(
                    """
                    SELECT vector_dims(e.embedding)
                    FROM langchain_pg_embedding e
                    JOIN langchain_pg_collection c ON e.collection_id = c.uuid
                    WHERE c.name = %s LIMIT 1
                    """,
                    (collection,),
                )
                r2 = cur.fetchone()
                if r2 and r2[0]:
                    return _provider_from_dim(int(r2[0]))
    except Exception:
        return None
    return None


def _raw_conn_string() -> str:
    # psycopg.connect wants a plain postgresql:// URL (no +psycopg driver suffix)
    return get_conn_string().replace("postgresql+psycopg://", "postgresql://")


def check_connection() -> tuple[bool, str]:
    """Return (ok, message). Friendly diagnostics when the DB isn't reachable."""
    try:
        import psycopg

        with psycopg.connect(_raw_conn_string(), connect_timeout=5):
            return True, "connected"
    except Exception as exc:  # noqa: BLE001
        return False, (
            f"Cannot reach the vector DB ({exc}). "
            "Start it with:  docker compose up -d   "
            "(and make sure Docker Desktop is running)."
        )


def list_collections() -> list[str]:
    """List existing code-to-spec collections, with row counts when available."""
    try:
        import psycopg

        with psycopg.connect(_raw_conn_string(), connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM langchain_pg_collection ORDER BY name")
                return [r[0] for r in cur.fetchall()]
    except Exception:
        return []
