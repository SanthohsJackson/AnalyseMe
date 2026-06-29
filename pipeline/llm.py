"""LLM client helpers for the code-to-spec pipeline."""

import json
import os
import re
import time

from langchain_core.messages import HumanMessage

from pipeline import cache


def get_provider() -> str:
    """Active LLM provider key (see pipeline.model_catalog.PROVIDERS)."""
    return os.environ.get("LLM_PROVIDER", "ollama").strip().lower()


def get_model_id() -> str:
    """Resolve the chat model id: explicit MODEL_ID, else provider default."""
    from pipeline.model_catalog import default_model

    return os.environ.get("MODEL_ID") or default_model(get_provider())


def get_llm(temperature: float = 0):
    from pipeline.model_catalog import provider_config

    provider = get_provider()
    cfg = provider_config(provider)
    model = get_model_id()

    if cfg["client"] == "ollama":
        from langchain_ollama import ChatOllama  # type: ignore

        base_url = os.environ.get("OLLAMA_BASE_URL", cfg["base_url"])
        return ChatOllama(model=model, temperature=temperature, base_url=base_url)

    # OpenAI-compatible: one path for OpenAI, DeepSeek, OpenRouter, xAI, Groq, …
    from langchain_openai import ChatOpenAI  # type: ignore

    kwargs = {"model": model, "temperature": temperature}
    base_url = os.environ.get("OPENAI_BASE_URL") or cfg.get("base_url")
    if base_url:
        kwargs["base_url"] = base_url
    api_key_env = cfg.get("api_key_env")
    if api_key_env and os.environ.get(api_key_env):
        kwargs["api_key"] = os.environ[api_key_env]
    return ChatOpenAI(**kwargs)


def _invoke_with_retry(llm, messages, max_conn_retries: int = 5):
    """Invoke the LLM, retrying on transient connection errors.

    Ollama can briefly drop connections (server busy, model reload, OOM
    restart). Back off and retry rather than crashing the whole pipeline.
    """
    last_exc = None
    for attempt in range(max_conn_retries):
        try:
            return llm.invoke(messages)
        except Exception as exc:  # noqa: BLE001 — inspect message for conn errors
            msg = str(exc).lower()
            is_conn = any(s in msg for s in (
                "connection refused", "connection error", "errno 61",
                "connecterror", "max retries", "timed out", "timeout",
                "remote end closed", "connection reset", "rate limit", "429",
            ))
            if not is_conn:
                raise
            last_exc = exc
            wait = min(2 ** attempt, 30)
            time.sleep(wait)
    hint = ("Is `ollama serve` running?" if get_provider() == "ollama"
            else "Check OPENAI_API_KEY and network connectivity.")
    raise RuntimeError(
        f"LLM provider unreachable after {max_conn_retries} retries. {hint} Last error: {last_exc}"
    )


def _extract_json_from_text(text: str) -> str:
    """Strip markdown code fences and return raw JSON text."""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return text.strip()


def _try_repair_json(text: str) -> str:
    """Best-effort repair of truncated JSON by closing open brackets/braces."""
    # Count unclosed structures
    stack = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]" and stack:
            stack.pop()
    # Close any open string first
    if in_string:
        text += '"'
    # Close open structures in reverse order
    text += "".join(reversed(stack))
    return text


def call_llm_json(prompt: str, max_retries: int = 2) -> dict | list:
    """Call LLM and parse a JSON object or array from the response (cached)."""
    key = cache.make_key("json", get_provider(), get_model_id(), prompt)
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = _call_llm_json_uncached(prompt, max_retries)
    cache.set(key, result)
    return result


def _call_llm_json_uncached(prompt: str, max_retries: int = 2) -> dict | list:
    """Call LLM and parse a JSON object or array from the response.

    On truncated JSON, attempts repair then retries with a shorter prompt.
    """
    llm = get_llm()
    messages = [HumanMessage(content=prompt)]

    for attempt in range(max_retries + 1):
        response = _invoke_with_retry(llm, messages)
        text = _extract_json_from_text(response.content)

        # First try parsing as-is
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try repairing truncated JSON
        try:
            return json.loads(_try_repair_json(text))
        except json.JSONDecodeError:
            pass

        # Ask the model to continue completing the JSON
        if attempt < max_retries:
            messages = [
                HumanMessage(content=prompt),
                response,
                HumanMessage(content=(
                    "Your previous response was cut off before the JSON was complete. "
                    "Please output ONLY the complete, valid JSON — no explanation, no markdown fences."
                )),
            ]

    raise ValueError(f"Failed to get valid JSON after {max_retries + 1} attempts. Last response:\n{text[:500]}")


def call_llm_structured(prompt: str, schema, max_retries: int = 2):
    """Call the LLM and return a validated instance of `schema` (a pydantic model).

    Uses the provider's native structured-output / JSON-schema mode, which
    constrains the model to the schema's keys — it cannot emit unknown top-level
    fields, which directly limits hallucination. Falls back to free-form JSON
    parsing + pydantic validation if the provider/runtime can't do structured
    output (pydantic still drops unknown keys on validation). Cached on disk.
    """
    key = cache.make_key("structured", get_provider(), get_model_id(), schema.__name__, prompt)
    cached = cache.get(key)
    if cached is not None:
        try:
            return schema.model_validate(cached)
        except Exception:
            pass  # stale/incompatible entry — recompute

    result = _call_llm_structured_uncached(prompt, schema, max_retries)
    cache.set(key, result.model_dump())
    return result


def _call_llm_structured_uncached(prompt: str, schema, max_retries: int = 2):
    llm = get_llm()
    messages = [HumanMessage(content=prompt)]

    try:
        structured = llm.with_structured_output(schema)
    except Exception:
        structured = None

    if structured is not None:
        try:
            result = _invoke_with_retry(structured, messages)
            return result if isinstance(result, schema) else schema.model_validate(result)
        except Exception:
            pass  # fall through to manual JSON parsing

    data = _call_llm_json_uncached(prompt, max_retries=max_retries)
    return schema.model_validate(data)


def call_llm_text(prompt: str) -> str:
    """Call LLM and return raw text response (cached)."""
    key = cache.make_key("text", get_provider(), get_model_id(), prompt)
    cached = cache.get(key)
    if cached is not None:
        return cached
    llm = get_llm()
    response = _invoke_with_retry(llm, [HumanMessage(content=prompt)])
    cache.set(key, response.content)
    return response.content
