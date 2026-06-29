import os
from pathlib import Path

import questionary
from rich.console import Console

console = Console()


def ask_repo_path() -> str:
    """Prompt for a local repo path OR a git URL to clone."""
    from pipeline.repo_source import is_git_url

    def _valid(val: str) -> bool | str:
        v = val.strip()
        if not v:
            return "Enter a local path or a git URL"
        if Path(v).expanduser().is_dir() or is_git_url(v):
            return True
        return "Must be an existing directory or a git URL (e.g. https://github.com/owner/repo)"

    source = questionary.text(
        "Repository to analyse (local path or git URL):",
        validate=_valid,
        style=questionary.Style([("text", "fg:green"), ("highlighted", "noinherit")]),
    ).ask()
    if not source:
        console.print("[red]No repository provided. Exiting...[/red]")
        exit(1)
    return source.strip()


def ask_output_file() -> str:
    default = "spec.md"
    val = questionary.text(
        "Output file name:",
        default=default,
    ).ask()
    return val or default


def ask_provider() -> str:
    """Choose the LLM provider from the catalog."""
    from pipeline.model_catalog import list_providers

    choice = questionary.select(
        "LLM provider:",
        choices=[questionary.Choice(label, value=key) for key, label in list_providers()],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
        ]),
    ).ask()
    return choice or "ollama"


def ask_model(provider: str) -> str:
    """Pick a model for the given provider (catalog choices + custom)."""
    import os
    from pipeline.model_catalog import provider_config, get_model_options, default_model

    cfg = provider_config(provider)

    # Warn early if the provider's API key is missing
    key_env = cfg.get("api_key_env")
    if key_env and not os.environ.get(key_env):
        console.print(f"[yellow]{key_env} is not set — add it to .env or your environment.[/yellow]")

    # Ollama: fetch the live model list from the daemon
    if cfg["client"] == "ollama":
        return ask_ollama_model()

    options = get_model_options(provider)
    if not options:
        return questionary.text(
            f"Enter {provider} model id:", default=default_model(provider)
        ).ask().strip()

    choice = questionary.select(
        f"{provider} model:",
        choices=[questionary.Choice(disp, value=val) for disp, val in options],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
        ]),
    ).ask()
    if choice == "custom" or choice is None:
        return questionary.text(
            f"Enter {provider} model id:", default=default_model(provider)
        ).ask().strip()
    return choice


def ask_ollama_model() -> str:
    """Fetch available Ollama models and prompt for selection."""
    import requests

    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    choices = []
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        models = [m["name"] for m in resp.json().get("models", [])]
        choices = [questionary.Choice(m, value=m) for m in models]
    except Exception:
        pass

    choices.append(questionary.Choice("Custom model ID", value="custom"))

    choice = questionary.select(
        "Select Ollama model:",
        choices=choices or [
            questionary.Choice("gemma4:e4b", value="gemma4:e4b"),
            questionary.Choice("Custom model ID", value="custom"),
        ],
        style=questionary.Style([
            ("selected", "fg:green noinherit"),
            ("highlighted", "fg:green noinherit"),
        ]),
    ).ask()

    if choice == "custom" or choice is None:
        custom = questionary.text("Enter model ID:", default="gemma4:e4b").ask()
        return (custom or "gemma4:e4b").strip()
    return choice


def ask_max_files() -> int | None:
    """Prompt for an optional file cap."""
    choice = questionary.select(
        "File cap (limit LLM calls for large repos):",
        choices=[
            questionary.Choice("All files (no cap)", value="all"),
            questionary.Choice("20 files", value="20"),
            questionary.Choice("50 files", value="50"),
            questionary.Choice("100 files", value="100"),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
        ]),
    ).ask()
    if not choice or choice == "all":
        return None
    return int(choice)


def ask_skip_tests() -> bool:
    """Prompt whether to skip test files."""
    result = questionary.confirm("Skip test files?", default=True).ask()
    return result if result is not None else True


def ask_analysis_passes() -> int:
    """Prompt for how many completeness-refinement passes to allow."""
    choice = questionary.select(
        "Analysis refinement passes (re-analyse under-captured units):",
        choices=[
            questionary.Choice("0 — single pass (fastest)", value="0"),
            questionary.Choice("1 — one refinement pass (recommended)", value="1"),
            questionary.Choice("2 — two refinement passes", value="2"),
            questionary.Choice("3 — three refinement passes (most thorough, slowest)", value="3"),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
        ]),
    ).ask()
    return int(choice) if choice else 1
