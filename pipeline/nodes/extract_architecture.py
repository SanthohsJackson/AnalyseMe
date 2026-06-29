"""
extract_architecture node: derives data schemas and cross-cutting concerns
from module summaries.
"""

import json
import os

from state_schema import CrossCutting, DataSchema, PipelineState

from pipeline.prompts.prompts import EXTRACT_ARCHITECTURE_PROMPT
from pipeline.llm import call_llm_json
from pipeline.nodes.ingest import is_third_party
from pipeline.parsers.tree_sitter_parser import extract_class_fields

# Keyword cues for classifying unit-level evidence into cross-cutting concerns.
_LOG_KW = ("log", "logger", "logging")
_CONC_KW = ("thread", "async", "await", "asyncio", "semaphore", "concurrent",
            "lock", "queue", "parallel", "coroutine", "future")
_CFG_KW = ("config", "environ", "env var", "settings", "getenv", ".env", "os.environ")
_EVIDENCE_CAP = 20  # cap each evidence list so the prompt stays bounded


def _aggregate_evidence(unit_analyses, dep_manifest) -> dict:
    """Pull cross-cutting evidence out of the rich per-unit analyses.

    The module summaries drop this detail, so error handling (raises), logging /
    concurrency (side effects + idioms), config, and external deps are gathered
    here directly from the units — deterministic, no LLM."""
    err, log, conc, cfg = [], [], [], []
    external: set[str] = set()

    for ua in unit_analyses:
        external.update(ua.external_deps)
        for iface in ua.interfaces:
            if iface.raises:
                err.append(f"{ua.path}::{iface.name} raises {', '.join(iface.raises)}")
            for se in iface.side_effects:
                s = se.lower()
                if any(k in s for k in _LOG_KW):
                    log.append(f"{ua.path}::{iface.name}: {se}")
                if any(k in s for k in _CONC_KW):
                    conc.append(f"{ua.path}::{iface.name}: {se}")
        notes = "; ".join(ua.idioms + ua.behavioral_notes)
        low = notes.lower()
        if any(k in low for k in _CONC_KW):
            conc.append(f"{ua.path}: {notes[:160]}")
        if any(k in low for k in _CFG_KW):
            cfg.append(f"{ua.path}: {notes[:160]}")

    for manifest in (dep_manifest or {}).values():
        external.update(manifest.get("dependencies", []))

    # Keep only genuine third-party packages (drop stdlib: json, datetime, enum…).
    external = {d for d in external if is_third_party(d)}

    return {
        "error_handling": err[:_EVIDENCE_CAP],
        "logging": log[:_EVIDENCE_CAP],
        "concurrency": conc[:_EVIDENCE_CAP],
        "config": cfg[:_EVIDENCE_CAP],
        "external_libraries": sorted(external)[:_EVIDENCE_CAP],
    }


def _deterministic_schemas(state: PipelineState) -> list[DataSchema]:
    """Build data schemas from REAL class fields (tree-sitter), not LLM guesses.

    Each data-model class (one with annotated fields) becomes a schema whose
    properties are its actual fields/types; the description reuses the class's
    analysed intent when available."""
    repo = state.get("repo_path", "")
    units = state.get("unit_analyses", [])

    intents = {
        iface.name: iface.intent
        for ua in units for iface in ua.interfaces
        if iface.name and iface.intent
    }

    schemas: list[DataSchema] = []
    seen: set[str] = set()
    for ua in units:
        for cname, fields in extract_class_fields(os.path.join(repo, ua.path)).items():
            if cname in seen:
                continue
            seen.add(cname)
            props = {f["name"]: {"type": f["type"] or "any"} for f in fields}
            schemas.append(DataSchema(
                name=cname,
                description=intents.get(cname, ""),
                json_schema={"type": "object", "properties": props},
            ))
    return schemas


def extract_architecture(state: PipelineState) -> dict:
    module_summaries = state.get("module_summaries", [])
    evidence = _aggregate_evidence(
        state.get("unit_analyses", []), state.get("dependency_manifest", {})
    )

    modules_data = [
        {
            "module_id": m.module_id,
            "name": m.name,
            "responsibility": m.responsibility,
            "public_surface": m.public_surface,
            "collaborators": m.collaborators,
        }
        for m in module_summaries
    ]

    # Phase 7 RAG: retrieve schema/cross-cutting-relevant modules when large.
    from pipeline.rag import select_context

    full_json = json.dumps(modules_data, indent=2)
    records = [
        {
            "id": m.module_id,
            "full": json.dumps(md, indent=2),
            "compact": f"{m.name}: {(m.responsibility or '')[:120]}",
        }
        for m, md in zip(module_summaries, modules_data)
    ]
    modules_ctx, _ = select_context(
        full_json, records,
        query="data schemas, data models, error handling, configuration, logging, "
              "authentication, concurrency, external integrations",
    )

    prompt = EXTRACT_ARCHITECTURE_PROMPT.format(
        modules_json=modules_ctx,
        evidence=json.dumps(evidence, indent=2),
    )

    raw = call_llm_json(prompt)

    # Prefer real, field-accurate schemas extracted from the code. Fall back to
    # the LLM's schemas only when no annotated data classes were found (e.g. a
    # non-Python repo the field extractor doesn't cover yet).
    data_schemas = _deterministic_schemas(state)
    if not data_schemas:
        for schema_data in raw.get("data_schemas", []):
            try:
                data_schemas.append(DataSchema(
                    name=schema_data.get("name", ""),
                    description=schema_data.get("description", ""),
                    json_schema=schema_data.get("json_schema", {}),
                ))
            except Exception:
                pass

    cc_data = raw.get("cross_cutting", {})
    cross_cutting = CrossCutting(
        error_handling=cc_data.get("error_handling", ""),
        config=cc_data.get("config", ""),
        logging=cc_data.get("logging", ""),
        auth=cc_data.get("auth", ""),
        concurrency=cc_data.get("concurrency", ""),
        external_integrations=cc_data.get("external_integrations", []),
    )

    # Grounded fallback: if the model left a concern empty but we have concrete
    # unit-level evidence for it, fill it deterministically so the detail isn't lost.
    def _summary(items: list[str], n: int = 5) -> str:
        return "; ".join(items[:n]) + (" …" if len(items) > n else "")

    if not cross_cutting.error_handling.strip() and evidence["error_handling"]:
        cross_cutting.error_handling = "Interfaces raise explicit exceptions, e.g. " + _summary(evidence["error_handling"])
    if not cross_cutting.logging.strip() and evidence["logging"]:
        cross_cutting.logging = "Logging observed as a side effect in: " + _summary(evidence["logging"])
    if not cross_cutting.concurrency.strip() and evidence["concurrency"]:
        cross_cutting.concurrency = "Concurrency primitives observed in: " + _summary(evidence["concurrency"])
    if not cross_cutting.config.strip() and evidence["config"]:
        cross_cutting.config = "Configuration handling observed in: " + _summary(evidence["config"])
    # NOTE: deliberately do NOT backfill external_integrations from library deps —
    # libraries (langchain, pydantic, …) are not runtime integrations. Package
    # dependencies are surfaced in the inventory instead; external_integrations is
    # reserved for actual external services the LLM identifies from evidence.

    return {"data_schemas": data_schemas, "cross_cutting": cross_cutting}
