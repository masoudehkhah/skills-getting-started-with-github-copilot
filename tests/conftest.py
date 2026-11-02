"""Shared pytest fixtures for the backend test suite."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a TestClient bound to the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities database after each test.

    Signup mutates the module-level ``activities`` dict, so snapshot it
    before each test and restore it afterwards to keep tests isolated.
    """
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
