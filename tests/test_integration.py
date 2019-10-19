"""Integration tests."""

import typing
from unittest import mock

import pytest
import sqlalchemy
from sqlalchemy.ext import declarative

import openapi_sqlalchemy


@pytest.mark.prod_env
@pytest.mark.integration
def test_empty_spec():
    """
    GIVEN empty specification
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(openapi_sqlalchemy.exceptions.MalformedSpecificationError):
        openapi_sqlalchemy.init_model_factory(base=None, spec={})


@pytest.mark.prod_env
@pytest.mark.integration
def test_empty_components():
    """
    GIVEN specification with empty components
    WHEN init_model_factory is called with the specification
    THEN KeyError is raised.
    """
    with pytest.raises(openapi_sqlalchemy.exceptions.MalformedSpecificationError):
        openapi_sqlalchemy.init_model_factory(base=None, spec={"components": {}})


@pytest.mark.prod_env
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


@pytest.mark.prod_env
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


@pytest.mark.prod_env
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


@pytest.mark.prod_env
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
def test_database_types(
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


@pytest.mark.prod_env
@pytest.mark.parametrize("index", ["x-primary-key", "x-index", "x-unique"])
@pytest.mark.integration
def test_database_indexes(engine, index: str):
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
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
    model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_autoincrement(engine, sessionmaker):
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
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
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


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_not_autoincrement(engine, sessionmaker):
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
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    model_instance = model(name="table name 1")
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.orm.exc.FlushError):
        session.flush()


@pytest.mark.prod_env
@pytest.mark.integration
def test_database_many_to_one_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with an object relationship
    WHEN schema is created, values inserted in both tables and queried
    THEN the data is returned as it was inserted.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "RefTable": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                    },
                    "x-tablename": "ref_table",
                    "x-backref": "tables",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table": {"$ref": "#/components/schemas/RefTable"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    ref_model = model_factory(name="RefTable")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance = ref_model(id=11, name="ref table name 1")
    model_instance = model(id=12, name="table name 1", ref_table=ref_model_instance)
    session = sessionmaker()
    session.add(ref_model_instance)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.name == "table name 1"
    assert queried_model.ref_table_id == 11
    assert queried_model.ref_table.id == 11
    assert queried_model.ref_table.name == "ref table name 1"
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.id == 11
    assert queried_ref_model.name == "ref table name 1"
    assert len(queried_ref_model.tables) == 1
    assert queried_ref_model.tables[0].id == 12


@pytest.mark.parametrize(
    "spec",
    [
        {
            "components": {
                "schemas": {
                    "Column": {"type": "integer", "x-primary-key": True},
                    "Table": {
                        "properties": {
                            "column": {"$ref": "#/components/schemas/Column"}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {"$ref": "#/components/schemas/RefTable"},
                    "RefTable": {
                        "properties": {
                            "column": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {
                            "column": {
                                "allOf": [{"type": "integer", "x-primary-key": True}]
                            }
                        },
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
        {
            "components": {
                "schemas": {
                    "Table": {
                        "allOf": [
                            {
                                "properties": {
                                    "column": {"type": "integer", "x-primary-key": True}
                                },
                                "x-tablename": "table",
                                "type": "object",
                            }
                        ]
                    }
                }
            }
        },
    ],
    ids=["ref column", "ref model", "allOf column", "allOf model"],
)
@pytest.mark.integration
def test_database_feature(engine, sessionmaker, spec):
    """
    GIVEN specification with a schema that has a $ref on a column
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = openapi_sqlalchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating model instance
    model_instance = model(column=1)
    session = sessionmaker()
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.column == 1
