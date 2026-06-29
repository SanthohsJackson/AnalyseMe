"""
Cross-run memory for code-to-spec.

Append-only markdown log of past analysis runs, keyed by repo. Its main job is
to remember the hallucinations the consistency reviewer caught so the next run
of the same repo can be warned not to repeat them — turning the review agent's
findings into durable lessons.

Adapted from TradingAgents' TradingMemoryLog: HTML-comment delimiters that can't
appear in LLM prose, atomic temp-file writes so a crash never corrupts the log,
and oldest-entry rotation.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

# HTML comment: cannot appear in LLM prose output, safe as a hard delimiter
_SEPARATOR = "\n\n<!-- ENTRY_END -->\n\n"

DEFAULT_MEMORY_PATH = Path("~/.code-to-spec/run_memory.md").expanduser()


class RunMemory:
    """Append-only markdown memory of past spec-generation runs."""

    def __init__(self, path: str | os.PathLike | None = None, max_entries: int | None = 50):
        self._path = Path(path).expanduser() if path else DEFAULT_MEMORY_PATH
        self._max_entries = max_entries

    # ---- write ----

    def store_run(
        self,
        repo_path: str,
        model: str,
        languages: list[str],
        unit_count: int,
        hallucinations: list[str],
        reflection: str = "",
    ) -> None:
        """Append a run entry. Pure I/O, no LLM call."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y-%m-%dT%H:%M")
            verdict = "grounded" if not hallucinations else f"{len(hallucinations)}flags"
            tag = f"[{ts} | {repo_path} | {model} | {','.join(languages) or '?'} | units={unit_count} | {verdict}]"

            parts = [tag]
            if hallucinations:
                parts.append("HALLUCINATIONS_CAUGHT:\n" + "\n".join(f"- {h}" for h in hallucinations))
            if reflection.strip():
                parts.append(f"REFLECTION:\n{reflection.strip()}")
            entry = "\n\n".join(parts)

            existing = self._path.read_text(encoding="utf-8") if self._path.exists() else ""
            blocks = [b for b in existing.split(_SEPARATOR) if b.strip()]
            blocks.append(entry)
            blocks = self._rotate(blocks)

            # Atomic write: temp file + replace
            tmp = self._path.with_suffix(".tmp")
            tmp.write_text(_SEPARATOR.join(blocks) + _SEPARATOR, encoding="utf-8")
            tmp.replace(self._path)
        except OSError:
            pass  # memory is best-effort; never break a run over it

    # ---- read ----

    def _load_blocks(self) -> list[str]:
        if not self._path.exists():
            return []
        text = self._path.read_text(encoding="utf-8")
        return [b.strip() for b in text.split(_SEPARATOR) if b.strip()]

    def get_past_context(self, repo_path: str, n: int = 3) -> str:
        """Return formatted lessons from prior runs of this repo for prompt injection.

        Focuses on previously-caught hallucinations so the model can avoid them.
        Returns "" when there is nothing useful to inject.
        """
        prefix = f"| {repo_path} |"
        matching = [b for b in self._load_blocks() if prefix in b.splitlines()[0]]
        if not matching:
            return ""

        lessons: list[str] = []
        for block in reversed(matching[-n:]):
            for line in block.splitlines():
                s = line.strip()
                if s.startswith("- "):       # a caught hallucination
                    lessons.append(s[2:])
        # De-duplicate while preserving order
        seen: set[str] = set()
        unique = [x for x in lessons if not (x in seen or seen.add(x))]
        if not unique:
            return ""

        return (
            "PRIOR LESSONS — in previous runs of this exact codebase, the consistency reviewer "
            "flagged the following claims as unsupported by the code. Do NOT reintroduce them; "
            "only state what the current analysis supports:\n"
            + "\n".join(f"- {x}" for x in unique[:15])
        )

    # ---- helpers ----

    def _rotate(self, blocks: list[str]) -> list[str]:
        if not self._max_entries or self._max_entries <= 0:
            return blocks
        if len(blocks) <= self._max_entries:
            return blocks
        return blocks[-self._max_entries:]
