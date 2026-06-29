"""
Basic integration tests for the code-to-spec pipeline.
LLM calls are stubbed so tests run without an API key.
"""

import json
import os
import sys
import tempfile
import textwrap
from unittest.mock import MagicMock, patch

import pytest

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state_schema import (
    BehavioralTest,
    CrossCutting,
    DataSchema,
    FileMeta,
    FileKind,
    Interface,
    ModuleSummary,
    UnitAnalysis,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_temp_repo() -> str:
    """Create a tiny Python repo in a temp directory."""
    tmpdir = tempfile.mkdtemp()

    # main module
    with open(os.path.join(tmpdir, "main.py"), "w") as f:
        f.write(textwrap.dedent("""\
            \"\"\"Entry point.\"\"\"
            from calculator import add, subtract

            def run():
                print(add(1, 2))
                print(subtract(5, 3))

            if __name__ == "__main__":
                run()
        """))

    # calculator module
    with open(os.path.join(tmpdir, "calculator.py"), "w") as f:
        f.write(textwrap.dedent("""\
            \"\"\"Simple arithmetic functions.\"\"\"

            def add(a: int, b: int) -> int:
                \"\"\"Return sum of a and b.\"\"\"
                return a + b

            def subtract(a: int, b: int) -> int:
                \"\"\"Return a minus b.\"\"\"
                return a - b
        """))

    # utility module
    with open(os.path.join(tmpdir, "utils.py"), "w") as f:
        f.write(textwrap.dedent("""\
            \"\"\"Utility helpers.\"\"\"

            def format_result(value: float) -> str:
                \"\"\"Format a number for display.\"\"\"
                return f"Result: {value:.2f}"
        """))

    # requirements
    with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
        f.write("click>=8.0\n")

    return tmpdir


def _stub_unit_analysis_json(path: str = "calculator.py") -> dict:
    return {
        "purpose": "Provides basic arithmetic operations.",
        "interfaces": [
            {
                "name": "add",
                "signature": "def add(a: int, b: int) -> int",
                "kind": "function",
                "inputs": ["a: int — first operand", "b: int — second operand"],
                "outputs": ["int — sum of a and b"],
                "raises": [],
                "side_effects": [],
                "intent": "Return the sum of two integers.",
            }
        ],
        "internal_deps": [],
        "external_deps": [],
        "idioms": [],
        "behavioral_notes": [],
    }


def _stub_module_summary_json() -> dict:
    return {
        "responsibility": "Provides arithmetic utilities for the application.",
        "public_surface": ["add(a, b)", "subtract(a, b)"],
        "collaborators": [],
    }


def _stub_architecture_json() -> dict:
    return {
        "data_schemas": [
            {
                "name": "Number",
                "description": "A numeric value",
                "json_schema": {"type": "number"},
            }
        ],
        "cross_cutting": {
            "error_handling": "Exceptions propagate to caller.",
            "config": "No configuration layer.",
            "logging": "No logging.",
            "auth": "No auth.",
            "concurrency": "Single-threaded.",
            "external_integrations": [],
        },
    }


def _stub_tests_json() -> list:
    return [
        {
            "target_interface": "calculator.add",
            "given": "Two integers a=1, b=2",
            "when": "add(a, b) is called",
            "then": "Returns 3",
        }
    ]


def _stub_validate_json(passed: bool = True) -> dict:
    return {"passed": passed, "gaps": [] if passed else ["Missing subtract documentation"]}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestIngestNode:
    def test_ingest_finds_python_files(self):
        tmpdir = _make_temp_repo()
        from pipeline.nodes.ingest import ingest
        result = ingest({"repo_path": tmpdir, "max_parallelism": 8})

        assert "files" in result
        paths = [f.path for f in result["files"]]
        assert any("main.py" in p for p in paths)
        assert any("calculator.py" in p for p in paths)
        assert "python" in result["languages_detected"]
        assert any("main.py" in ep for ep in result["entry_points"])

    def test_ingest_parses_requirements(self):
        tmpdir = _make_temp_repo()
        from pipeline.nodes.ingest import ingest
        result = ingest({"repo_path": tmpdir, "max_parallelism": 8})
        assert result["dependency_manifest"]
        manifest_values = list(result["dependency_manifest"].values())
        assert any(m.get("type") == "python" for m in manifest_values)

    def test_ingest_classifies_source_kind(self):
        tmpdir = _make_temp_repo()
        from pipeline.nodes.ingest import ingest
        result = ingest({"repo_path": tmpdir, "max_parallelism": 8})
        source_files = [f for f in result["files"] if f.kind == FileKind.SOURCE]
        assert len(source_files) >= 3


class TestRouteUnitsNode:
    def test_route_units_creates_descriptors(self):
        tmpdir = _make_temp_repo()
        from pipeline.nodes.ingest import ingest
        from pipeline.nodes.route_units import route_units

        ingest_result = ingest({"repo_path": tmpdir, "max_parallelism": 8})
        state = {**ingest_result, "repo_path": tmpdir, "max_parallelism": 8}
        result = route_units(state)

        assert "units_to_analyze" in result
        units = result["units_to_analyze"]
        assert len(units) >= 3  # main, calculator, utils
        assert all("unit_id" in u for u in units)
        assert all("language" in u for u in units)

    def test_route_units_skips_non_source(self):
        tmpdir = _make_temp_repo()
        from pipeline.nodes.ingest import ingest
        from pipeline.nodes.route_units import route_units

        ingest_result = ingest({"repo_path": tmpdir, "max_parallelism": 8})
        state = {**ingest_result, "repo_path": tmpdir, "max_parallelism": 8}
        result = route_units(state)

        units = result["units_to_analyze"]
        # requirements.txt should not be included (it's BUILD kind)
        langs = [u["language"] for u in units]
        assert all(lang == "python" for lang in langs)


class TestAnalyzeUnitNode:
    def test_analyze_unit_success(self):
        tmpdir = _make_temp_repo()

        stub_response = MagicMock()
        stub_response.content = json.dumps(_stub_unit_analysis_json())

        with patch("pipeline.llm.get_llm") as mock_get_llm:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = stub_response
            mock_get_llm.return_value = mock_llm

            from pipeline.nodes.analyze_unit import analyze_unit
            descriptor = {
                "unit_id": "calculator_py",
                "path": "calculator.py",
                "language": "python",
                "repo_path": tmpdir,
                "large_file": False,
            }
            result = analyze_unit(descriptor)

        assert result["map_errors"] == []
        assert len(result["unit_analyses"]) == 1
        ua = result["unit_analyses"][0]
        assert isinstance(ua, UnitAnalysis)
        assert ua.purpose != ""
        assert len(ua.interfaces) >= 1

    def test_analyze_unit_handles_missing_file(self):
        from pipeline.nodes.analyze_unit import analyze_unit
        descriptor = {
            "unit_id": "nonexistent",
            "path": "nonexistent.py",
            "language": "python",
            "repo_path": "/tmp/does_not_exist_abc123",
            "large_file": False,
        }
        result = analyze_unit(descriptor)
        assert result["unit_analyses"] == []
        assert len(result["map_errors"]) == 1


class TestFullPipeline:
    """Integration test: run the full graph with stubbed LLM calls."""

    def _make_stub_llm(self, responses: list[str]):
        """Return an LLM mock that cycles through the given responses."""
        call_count = {"n": 0}
        stub_response = MagicMock()

        def side_effect(messages):
            idx = min(call_count["n"], len(responses) - 1)
            stub_response.content = responses[idx]
            call_count["n"] += 1
            return stub_response

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = side_effect
        return mock_llm

    def test_full_graph_produces_spec(self):
        tmpdir = _make_temp_repo()

        # Build response list: analyze×3, reduce×1, synthesize×1,
        # architecture×1, tests×1, assemble×1, validate×1
        unit_resp = json.dumps(_stub_unit_analysis_json())
        module_resp = json.dumps(_stub_module_summary_json())
        system_resp = "This system provides basic arithmetic via a calculator module."
        arch_resp = json.dumps(_stub_architecture_json())
        tests_resp = json.dumps(_stub_tests_json())
        assemble_resp = (
            "# Reimplementation Spec\n"
            "## 1. Inventory\nPython project with calculator utilities.\n"
            "## 7. Acceptance Tests\n- add(1,2) returns 3\n"
        )
        validate_resp = json.dumps(_stub_validate_json(passed=True))

        responses = (
            [unit_resp] * 10  # enough for all analyze_unit calls
            + [module_resp] * 5
            + [system_resp]
            + [arch_resp]
            + [tests_resp]
            + [assemble_resp]
            + [validate_resp]
        )

        mock_llm = self._make_stub_llm(responses)

        with patch("pipeline.llm.get_llm", return_value=mock_llm):
            from langgraph.checkpoint.memory import MemorySaver
            # Re-import graph to pick up patched llm
            import importlib
            import graph as graph_mod
            importlib.reload(graph_mod)

            checkpointer = MemorySaver()
            g = graph_mod.build_graph(checkpointer=checkpointer)

            initial_state = {
                "repo_path": tmpdir,
                "output_path": "/tmp/test_spec.md",
                "max_parallelism": 4,
                "revision_count": 0,
                "unit_analyses": [],
                "map_errors": [],
                "behavioral_tests": [],
            }

            import uuid
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}
            result = g.invoke(initial_state, config=config)

        assert len(result.get("unit_analyses", [])) > 0, "unit_analyses should be non-empty"
        assert result.get("system_overview", "") != "", "system_overview should be non-empty"
        doc = result.get("draft_document", "") or result.get("final_document", "")
        assert doc != "", "draft_document (or final_document) should be non-empty"
