"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access

import pytest

from openapi_sqlalchemy import model_factory


def test_missing_schema():
    """
    GIVEN schemas and name that is not in schemas
    WHEN model_factory is called
    THEN KeyError is raised.
    """
    with pytest.raises(KeyError):
        model_factory.model_factory(name="Missing", schemas={})


def test_missing_tablename():
    """
    GIVEN schemas and name that refers to a schema without the x-tablename key
    WHEN model_factory is called
    THEN TypeError is raised.
    """
    with pytest.raises(TypeError):
        model_factory.model_factory(
            name="MissingTablename", schemas={"MissingTablename": {}}
        )


def test_valid():
    """
    GIVEN schemas and name that is in schemas
    WHEN model_factory is called
    THEN no exception is raised.
    """
    model_factory.model_factory(
        name="Valid", schemas={"Valid": {"x-tablename": "table 1"}}
    )
