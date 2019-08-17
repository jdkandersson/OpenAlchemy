"""Integration tests."""

from unittest import mock

import pytest
import sqlalchemy

import openapi_sqlalchemy


@pytest.mark.integration
def test_empty_spec():
    """
    GIVEN empty specification
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(KeyError):
        openapi_sqlalchemy.init_model_factory(base=None, spec={})


@pytest.mark.integration
def test_empty_components():
    """
    GIVEN specification with empty components
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(KeyError):
        openapi_sqlalchemy.init_model_factory(base=None, spec={"components": {}})


@pytest.mark.integration
def test_cache_diff(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called with different names
    THEN mocked model_factory is called the same number of times the return value is
        called.
    """
    model_factory = openapi_sqlalchemy.init_model_factory(
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
    )

    model_factory(name="table 1")
    model_factory(name="table 2")

    assert mocked_model_factory.call_count == 2


@pytest.mark.integration
def test_cache_same(mocked_model_factory: mock.MagicMock):
    """
    GIVEN valid specification and mocked model_factory
    WHEN return value of init_model_factory is called multiple times with the same name
    THEN mocked model_factory is called once.
    """
    model_factory = openapi_sqlalchemy.init_model_factory(
        base=mock.MagicMock, spec={"components": {"schemas": {}}}
    )

    model_factory(name="table 1")
    model_factory(name="table 1")

    assert mocked_model_factory.call_count == 1


@pytest.mark.integration
def test_schema():
    """
    GIVEN valid specification with single property
    WHEN return value of init_model_factory is called with the name of the schema
    THEN a SQLAlchemy model with a single property is returned.
    """
    model_factory = openapi_sqlalchemy.init_model_factory(
        base=mock.MagicMock,
        spec={
            "components": {
                "schemas": {
                    "Table1": {
                        "properties": {"column_1": {"type": "integer"}},
                        "x-tablename": "table_1",
                        "type": "object",
                    }
                }
            }
        },
    )

    model = model_factory(name="Table1")

    # Checking model
    assert model.__tablename__ == "table_1"
    assert hasattr(model, "column_1")
    assert isinstance(model.column_1.type, sqlalchemy.Integer)
