"""Shared fixtures for tests."""

from unittest import mock

import pytest
import sqlalchemy

from openapi_sqlalchemy import column_factory
from openapi_sqlalchemy import model_factory


@pytest.fixture
def mocked_sqlalchemy_column(monkeypatch):
    """Monkeypatches sqlalchemy.Column."""
    mock_column = mock.MagicMock()
    monkeypatch.setattr(sqlalchemy, "Column", mock_column)
    return mock_column


@pytest.fixture
def mocked_sqlalchemy_string(monkeypatch):
    """Monkeypatches sqlalchemy.String."""
    mock_string = mock.MagicMock()
    monkeypatch.setattr(sqlalchemy, "String", mock_string)
    return mock_string


@pytest.fixture
def mocked_column_factory(monkeypatch):
    """Monkeypatches column_factory.column_factory."""
    mock_column_factory = mock.MagicMock()
    monkeypatch.setattr(column_factory, "column_factory", mock_column_factory)
    return mock_column_factory


@pytest.fixture
def mocked_model_factory(monkeypatch):
    """Monkeypatches model_factory.model_factory."""
    mock_model_factory = mock.MagicMock()
    monkeypatch.setattr(model_factory, "model_factory", mock_model_factory)
    return mock_model_factory
