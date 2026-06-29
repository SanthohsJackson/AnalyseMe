"""Content-addressed on-disk cache for LLM calls.

Calls are deterministic (temperature=0), so the same (provider, model, prompt)
always yields the same response. Caching it makes dev re-runs, the multi-pass
refinement loop, and the critic revision loop near-instant on repeated prompts.

Enabled by default; set LLM_CACHE=0 (or false/no/off) to disable. The cache
directory defaults to ./.llm_cache and can be overridden with LLM_CACHE_DIR.
Each entry is a small JSON file named by the sha256 of its key parts.
"""

import hashlib
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

_DISABLED_VALUES = {"0", "false", "no", "off", ""}


def enabled() -> bool:
    return os.environ.get("LLM_CACHE", "1").strip().lower() not in _DISABLED_VALUES


def cache_dir() -> Path:
    d = Path(os.environ.get("LLM_CACHE_DIR", ".llm_cache"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def make_key(*parts: str) -> str:
    """Hash the given parts into a stable cache key (order-sensitive)."""
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\x00")  # delimiter so ("ab","c") != ("a","bc")
    return h.hexdigest()


def get(key: str):
    """Return the cached value for `key`, or None on miss/disabled/error."""
    if not enabled():
        return None
    path = cache_dir() / f"{key}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.debug("cache read failed for %s: %s", key, exc)
        return None


def set(key: str, value) -> None:  # noqa: A001 — mirror dict-like get/set naming
    """Persist a JSON-serialisable `value` under `key` (no-op if disabled)."""
    if not enabled():
        return
    try:
        path = cache_dir() / f"{key}.json"
        # Write atomically so a crash mid-write can't leave a half file that
        # later reads as corrupt.
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(value), encoding="utf-8")
        tmp.replace(path)
    except Exception as exc:
        logger.debug("cache write failed for %s: %s", key, exc)


def clear() -> int:
    """Delete all cache entries. Returns the number of files removed."""
    if not Path(os.environ.get("LLM_CACHE_DIR", ".llm_cache")).exists():
        return 0
    n = 0
    for f in cache_dir().glob("*.json"):
        try:
            f.unlink()
            n += 1
        except OSError:
            pass
    return n
