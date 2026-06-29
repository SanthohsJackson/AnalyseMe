"""
Run reflection — adapted from TradingAgents' Reflector.

Produces a terse, plain-prose lesson about a completed spec run that is stored
in RunMemory and re-read on future runs. Kept compact (2-4 sentences) so it
doesn't bloat the context window when injected later.
"""

from pipeline.llm import call_llm_text

_REFLECT_PROMPT = (
    "You are reviewing a code-to-spec analysis run you just completed.\n"
    "Write exactly 2-4 sentences of plain prose (no bullets, no headers, no markdown).\n\n"
    "Cover, in order:\n"
    "1. What kind of project this is and what was captured.\n"
    "2. Where the analysis was weak or the reviewer caught invented content.\n"
    "3. One concrete lesson to apply next time this repo is analysed.\n\n"
    "Be specific and terse. Your output is stored verbatim in a memory log and re-read by "
    "future runs, so every word must earn its place."
)


def reflect_on_run(
    repo_name: str,
    languages: list[str],
    unit_count: int,
    hallucinations: list[str],
) -> str:
    """Single best-effort reflection call. Returns "" on failure."""
    findings = "\n".join(f"- {h}" for h in hallucinations) or "(none — the spec was fully grounded)"
    prompt = (
        f"{_REFLECT_PROMPT}\n\n"
        f"Project: {repo_name}\n"
        f"Languages: {', '.join(languages) or 'unknown'}\n"
        f"Units analysed: {unit_count}\n"
        f"Hallucinations the reviewer caught:\n{findings}"
    )
    try:
        return call_llm_text(prompt).strip()
    except Exception:
        return ""
