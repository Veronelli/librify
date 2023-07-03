import pytest

from main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest.fixture
def load_enviroment(monkeypatch):
    monkeypatch.setenv("MONGO_INITDB_ROOT_USERNAME", "TEST_USERNAME")
    monkeypatch.setenv("MONGO_INITDB_ROOT_PASSWORD", "TEST_PASSWORD")
    monkeypatch.setenv("SECRET_KEY", "SECRET_KEY")

@pytest.fixture
def app(load_enviroment: None):
    from main import app
    return app

@pytest.fixture
def app_client(app):
    return TestClient(app)

