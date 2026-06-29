"""Shared pytest fixtures/config for the pipeline tests."""

import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _disable_llm_cache():
    """Disable the on-disk LLM cache during tests.

    Tests stub the LLM and rely on each call hitting the (mocked) model; a
    persistent cache could serve stale responses across runs and would write
    files into the working tree.
    """
    prev = os.environ.get("LLM_CACHE")
    os.environ["LLM_CACHE"] = "0"
    yield
    if prev is None:
        os.environ.pop("LLM_CACHE", None)
    else:
        os.environ["LLM_CACHE"] = prev
