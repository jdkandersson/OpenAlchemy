"""Fixtures for utility base tests."""

from unittest import mock

import pytest

import open_alchemy


@pytest.fixture
def mocked_models(monkeypatch):
    """Monkeypatch open_alchemy.models"""
    mock_models = mock.MagicMock()
    monkeypatch.setattr(open_alchemy, "models", mock_models)
    yield mock_models
