"""Input validation tests."""
# Disable protected access for testing.
# pylint: disable=protected-access

import pytest

from openapi_sqlalchemy import model_factory


@pytest.mark.model
def test_missing_schema():
    """
    GIVEN schemas and name that is not in schemas
    WHEN model_factory is called
    THEN KeyError is raised.
    """
    with pytest.raises(KeyError):
        model_factory.model_factory(name="Missing", schemas={})


@pytest.mark.model
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


@pytest.mark.model
def test_not_object():
    """
    GIVEN schemas  with schema that is not an object
    WHEN model_factory is called with the name of the schema
    THEN NotImplementedError is raised.
    """
    with pytest.raises(NotImplementedError):
        model_factory.model_factory(
            name="NotObject",
            schemas={"NotObject": {"x-tablename": "table 1", "type": "not_object"}},
        )
