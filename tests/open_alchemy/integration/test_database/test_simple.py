"""Integration tests against database for simple tests."""

import copy
import datetime

import pytest
import sqlalchemy
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.parametrize(
    "type_, format_, value",
    [
        pytest.param(
            "integer",
            None,
            1,
            id="integer",
        ),
        pytest.param(
            "integer",
            "int32",
            1,
            id="int32",
        ),
        pytest.param(
            "integer",
            "int64",
            1,
            id="int64",
        ),
        pytest.param(
            "number",
            None,
            1.1,
            id="number",
        ),
        pytest.param(
            "number",
            "float",
            1.1,
            id="float",
        ),
        pytest.param(
            "string",
            None,
            "some string",
            id="string",
        ),
        pytest.param(
            "string",
            "password",
            "some password",
            id="password",
        ),
        pytest.param(
            "string",
            "byte",
            "some string",
            id="byte",
        ),
        pytest.param(
            "string",
            "binary",
            b"some bytes",
            id="binary",
        ),
        pytest.param(
            "string",
            "date",
            datetime.date(year=2000, month=1, day=1),
            id="date",
        ),
        pytest.param(
            "string",
            "date-time",
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
            id="date-time",
        ),
        pytest.param(
            "string",
            "unsupported",
            "some password",
            id="unsupported",
        ),
        pytest.param(
            "boolean",
            None,
            True,
            id="boolean",
        ),
    ],
)
@pytest.mark.integration
def test_types(engine, sessionmaker, type_, format_, value):
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
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
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


@pytest.mark.parametrize(
    "schema, value",
    [
        pytest.param({"type": "integer", "x-json": True}, 1, id="integer"),
        pytest.param({"type": "number", "x-json": True}, 1.1, id="number"),
        pytest.param(
            {"type": "string", "x-json": True},
            "value 1",
            id="string",
        ),
        pytest.param(
            {"type": "boolean", "x-json": True},
            True,
            id="boolean",
        ),
        pytest.param(
            {"type": "object", "x-json": True},
            {"key": "value"},
            id="object",
        ),
        pytest.param({"type": "array", "x-json": True}, [1], id="array"),
    ],
)
@pytest.mark.integration
def test_types_json(engine, sessionmaker, schema, value):
    """
    GIVEN specification with a schema with a JSON property
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "column": schema,
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(id=1, column=copy.deepcopy(value))
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == value


@pytest.mark.parametrize(
    "type_, format_, default, expected_value",
    [
        ("integer", None, 1, 1),
        ("integer", "int32", 1, 1),
        ("integer", "int64", 1, 1),
        ("number", None, 1.1, 1.1),
        ("number", "float", 1.1, 1.1),
        ("string", None, "some string", "some string"),
        ("string", "password", "some password", "some password"),
        ("string", "byte", "some string", "some string"),
        ("string", "binary", "some bytes", b"some bytes"),
        ("string", "date", "2000-01-01", datetime.date(year=2000, month=1, day=1)),
        (
            "string",
            "date-time",
            "2000-01-01T01:01:01",
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
        ("boolean", None, True, True),
    ],
    ids=[
        "integer",
        "int32",
        "int64",
        "number",
        "float",
        "string",
        "password",
        "byte",
        "binary",
        "date",
        "date-time",
        "boolean",
    ],
)
@pytest.mark.integration
def test_types_default(engine, sessionmaker, type_, format_, default, expected_value):
    """
    GIVEN specification with a schema with a given type column and a default for that
        column
    WHEN schema is created and an instance is added to the session
    THEN the instance with the default value is returned when the session is queried for
        it.
    """
    # Defining specification
    column_schema = {"type": type_, "x-primary-key": True, "default": default}
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
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model()
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == expected_value


@pytest.mark.parametrize("index", ["x-primary-key", "x-index", "x-unique"])
@pytest.mark.integration
def test_indexes(engine, index: str):
    """
    GIVEN specification with a schema with an integer and given index
    WHEN schema is created
    THEN no exceptions get raised.
    """
    # Defining specification
    column_schema = {"type": "integer", index: True}
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "column": column_schema,
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)


@pytest.mark.integration
def test_autoincrement(engine, sessionmaker):
    """
    GIVEN specification with a schema with an autoincrement id column
    WHEN schema is created, values inserted without id column
    THEN the data is returned as it was inserted with autogenerated value.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": True,
                        },
                        "name": {"type": "string"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(name="table name 1")
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 1
    assert queried_model.name == "table name 1"


@pytest.mark.integration
def test_not_autoincrement(engine, sessionmaker):
    """
    GIVEN specification with a schema with autoincrement disabled id column
    WHEN schema is created, values inserted without id column
    THEN exception is raised.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": False,
                        },
                        "name": {"type": "string"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(name="table name 1")
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.orm.exc.FlushError):
        session.flush()


@pytest.mark.integration
def test_default(engine, sessionmaker):
    """
    GIVEN specification with a schema with a default value for a column
    WHEN schema is created, values inserted without value for the default column
    THEN the data is returned as it was inserted with default value.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string", "default": "name 1"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(id=1)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 1
    assert queried_model.name == "name 1"
