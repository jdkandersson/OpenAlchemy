"""Shared fixtures for tests."""
# pylint: disable=redefined-outer-name

from unittest import mock
from urllib import request

import pytest
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import column_factory
from open_alchemy import helpers
from open_alchemy import model_factory
from open_alchemy import models


@pytest.fixture
def mocked_column_factory(monkeypatch):
    """Monkeypatches column_factory.column_factory."""
    mock_column_factory = mock.MagicMock()
    mock_column_factory.return_value = ([("logical name", "SQLAlchemy column")], {})
    monkeypatch.setattr(column_factory, "column_factory", mock_column_factory)
    return mock_column_factory


@pytest.fixture
def mocked_model_factory(monkeypatch):
    """Monkeypatches model_factory.model_factory."""
    mock_model_factory = mock.MagicMock()
    monkeypatch.setattr(model_factory, "model_factory", mock_model_factory)
    return mock_model_factory


@pytest.fixture
def mocked_ref_resolve(monkeypatch):
    """Monkeypatches helpers.ref.resolve."""
    mock_ref_resolve = mock.MagicMock()
    mock_ref_resolve.return_value = (mock.MagicMock(), mock.MagicMock())
    monkeypatch.setattr(helpers.ref, "resolve", mock_ref_resolve)
    return mock_ref_resolve


@pytest.fixture
def _mocked_ref_resolve(mocked_ref_resolve):
    """Alias of mocked_ref_resolve to suppress unused argument."""
    return mocked_ref_resolve


@pytest.fixture
def mocked_handle_column(monkeypatch):
    """Mock column_factory._handle_column."""
    mock_handle_column = mock.MagicMock()
    monkeypatch.setattr(column_factory, "_handle_column", mock_handle_column)
    return mock_handle_column


@pytest.fixture
def _mocked_handle_column(mocked_handle_column):
    """Alias of mocked_handle_column to suppress unused argument."""
    return mocked_handle_column


@pytest.fixture(scope="function")
def args():
    """Arguments."""
    return ("arg1", "arg2")


@pytest.fixture(scope="function")
def kwargs():
    """Keyword arguments."""
    return {"kwarg1": "value 1", "kwarg2": "value 2"}


@pytest.fixture(scope="session")
def testing_env_name():
    """Environment variable name that indicates that tests are running."""
    return "TESTING"


@pytest.fixture(scope="session")
def decorator_trace_env_name():
    """Environment variable name where decorator traces are stored."""
    return "DECORATOR_TRACE"


@pytest.fixture
def mocked_init_model_factory(monkeypatch):
    """Monkeypatch open_alchemy.init_model_factory."""
    mock_init_model_factory = mock.MagicMock()
    monkeypatch.setattr(open_alchemy, "init_model_factory", mock_init_model_factory)
    return mock_init_model_factory


@pytest.fixture
def _mocked_init_model_factory(mocked_init_model_factory):
    """Used to hide unused argument error.."""
    return mocked_init_model_factory


@pytest.fixture
def mocked_declarative_base(monkeypatch):
    """Monkeypatch declarative.declarative_base."""
    mock_declarative_base = mock.MagicMock()
    monkeypatch.setattr(declarative, "declarative_base", mock_declarative_base)
    return mock_declarative_base


@pytest.fixture
def mocked_facades_models(monkeypatch):
    """Monkeypatch open_alchemy.facades.models."""
    mock_models = mock.MagicMock()
    monkeypatch.setattr(open_alchemy.facades, "models", mock_models)
    return mock_models


@pytest.fixture
def _mocked_facades_models(mocked_facades_models):
    """Suppress unused argument error."""
    return mocked_facades_models


@pytest.fixture
def mocked_facades_sqlalchemy(monkeypatch):
    """Monkeypatch open_alchemy.facades.sqlalchemy."""
    mock_sqlalchemy = mock.MagicMock()
    monkeypatch.setattr(open_alchemy.facades, "sqlalchemy", mock_sqlalchemy)
    return mock_sqlalchemy


@pytest.fixture(autouse=True)
def cleanup_models():
    """Remove any new attributes on open_alchemy.models."""
    for key in set(models.__dict__.keys()):
        if key.startswith("__"):
            continue
        if key.endswith("__"):
            continue
        delattr(models, key)

    yield

    for key in set(models.__dict__.keys()):
        if key.startswith("__"):
            continue
        if key.endswith("__"):
            continue
        delattr(models, key)


@pytest.fixture
def mocked_urlopen(monkeypatch):
    """Monkeypatches urlopen.urlopen."""
    mock_urlopen = mock.MagicMock()
    monkeypatch.setattr(request, "urlopen", mock_urlopen)
    return mock_urlopen
