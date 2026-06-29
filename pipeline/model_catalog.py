"""
Central model/provider catalog (modelled on TradingAgents' model_catalog).

Most hosted providers expose an OpenAI-compatible API, so they all run through
one ChatOpenAI path with a different base_url + API-key env var. Ollama is the
local option. Adding a provider is just a row here.
"""

from __future__ import annotations

# provider key -> config
#   client:      "ollama" | "openai-compatible"
#   base_url:    endpoint (None = OpenAI default)
#   api_key_env: env var holding the key (None for local)
PROVIDERS: dict[str, dict] = {
    "ollama": {
        "label": "Ollama (local, default)",
        "client": "ollama",
        "base_url": "http://localhost:11434",
        "api_key_env": None,
    },
    "openai": {
        "label": "OpenAI",
        "client": "openai-compatible",
        "base_url": None,
        "api_key_env": "OPENAI_API_KEY",
    },
    "deepseek": {
        "label": "DeepSeek",
        "client": "openai-compatible",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    "openrouter": {
        "label": "OpenRouter (many models)",
        "client": "openai-compatible",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
    },
    "xai": {
        "label": "xAI (Grok)",
        "client": "openai-compatible",
        "base_url": "https://api.x.ai/v1",
        "api_key_env": "XAI_API_KEY",
    },
    "groq": {
        "label": "Groq (fast inference)",
        "client": "openai-compatible",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
    },
    "together": {
        "label": "Together AI",
        "client": "openai-compatible",
        "base_url": "https://api.together.xyz/v1",
        "api_key_env": "TOGETHER_API_KEY",
    },
}

# Curated model choices per provider: (display, value). "custom" lets the user type any id.
_CUSTOM = ("Custom model id…", "custom")

MODEL_OPTIONS: dict[str, list[tuple[str, str]]] = {
    "openai": [
        ("gpt-4o-mini — fast, cheap (recommended)", "gpt-4o-mini"),
        ("gpt-4o — strong general model", "gpt-4o"),
        ("gpt-4.1 — smartest non-reasoning", "gpt-4.1"),
        ("gpt-4.1-mini — balanced", "gpt-4.1-mini"),
        ("o4-mini — reasoning, cost-effective", "o4-mini"),
        _CUSTOM,
    ],
    "deepseek": [
        ("deepseek-chat — general (V3)", "deepseek-chat"),
        ("deepseek-reasoner — reasoning (R1)", "deepseek-reasoner"),
        _CUSTOM,
    ],
    "openrouter": [
        ("openai/gpt-4o-mini", "openai/gpt-4o-mini"),
        ("anthropic/claude-3.5-sonnet", "anthropic/claude-3.5-sonnet"),
        ("google/gemini-2.0-flash-001", "google/gemini-2.0-flash-001"),
        ("meta-llama/llama-3.3-70b-instruct", "meta-llama/llama-3.3-70b-instruct"),
        _CUSTOM,
    ],
    "xai": [
        ("grok-2-latest", "grok-2-latest"),
        ("grok-beta", "grok-beta"),
        _CUSTOM,
    ],
    "groq": [
        ("llama-3.3-70b-versatile", "llama-3.3-70b-versatile"),
        ("llama-3.1-8b-instant — fastest", "llama-3.1-8b-instant"),
        ("qwen-2.5-coder-32b", "qwen-2.5-coder-32b"),
        _CUSTOM,
    ],
    "together": [
        ("meta-llama/Llama-3.3-70B-Instruct-Turbo", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),
        ("Qwen/Qwen2.5-Coder-32B-Instruct", "Qwen/Qwen2.5-Coder-32B-Instruct"),
        _CUSTOM,
    ],
    # ollama models are fetched live from the daemon at selection time
}

# Default chat model per provider when none specified
DEFAULT_MODEL: dict[str, str] = {
    "ollama": "gemma4:e4b",
    "openai": "gpt-4o-mini",
    "deepseek": "deepseek-chat",
    "openrouter": "openai/gpt-4o-mini",
    "xai": "grok-2-latest",
    "groq": "llama-3.3-70b-versatile",
    "together": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
}


def list_providers() -> list[tuple[str, str]]:
    return [(key, cfg["label"]) for key, cfg in PROVIDERS.items()]


def provider_config(provider: str) -> dict:
    return PROVIDERS.get(provider.lower(), PROVIDERS["ollama"])


def get_model_options(provider: str) -> list[tuple[str, str]]:
    return MODEL_OPTIONS.get(provider.lower(), [])


def default_model(provider: str) -> str:
    return DEFAULT_MODEL.get(provider.lower(), "gpt-4o-mini")
