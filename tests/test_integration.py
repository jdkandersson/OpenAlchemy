"""Integration tests."""

import typing
from unittest import mock

import pytest
import sqlalchemy
from sqlalchemy.ext import declarative

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
                    "Table": {
                        "properties": {"column": {"type": "integer"}},
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
    )

    model = model_factory(name="Table")

    # Checking model
    assert model.__tablename__ == "table"
    assert hasattr(model, "column")
    assert isinstance(model.column.type, sqlalchemy.Integer)


@pytest.mark.parametrize(
    "type_, format_, value",
    [
        ("integer", None, 1),
        ("integer", "int64", 1),
        ("number", None, 1.0),
        ("string", None, "some string"),
        ("boolean", None, True),
    ],
)
@pytest.mark.integration
def test_database_integer(
    engine, sessionmaker, type_: str, format_: typing.Optional[str], value: typing.Any
):
    """
    GIVEN specification with a schema with a given type column and a value for that
        column
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Defining specification
    column_schema = {"type": type_, "x-primary-key": True}
    if format_ is not None:
        column_schema["format"] = format_
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {"column": column_schema},
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=value)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value
