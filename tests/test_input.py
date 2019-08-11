"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access

import pytest

import openapi_sqlalchemy


def test_missing_schema():
    """
    GIVEN schemas and name that is not in schemas
    WHEN _model_factory is called
    THEN KeyError is raised.
    """
    with pytest.raises(KeyError):
        openapi_sqlalchemy._model_factory(name="Missing", schemas={})


def test_missing_tablename():
    """
    GIVEN schemas and name that refers to a schema without the x-tablename key
    WHEN _model_factory is called
    THEN TypeError is raised.
    """
    with pytest.raises(TypeError):
        openapi_sqlalchemy._model_factory(
            name="MissingTablename", schemas={"MissingTablename": {}}
        )


def test_valid():
    """
    GIVEN schemas and name that is in schemas
    WHEN _model_factory is called
    THEN no exception is raised.
    """
    openapi_sqlalchemy._model_factory(
        name="Valid", schemas={"Valid": {"x-tablename": "table 1"}}
    )
