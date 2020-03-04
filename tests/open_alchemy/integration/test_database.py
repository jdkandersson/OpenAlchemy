"""Integration tests against database."""

import datetime

import pytest
import sqlalchemy
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.parametrize(
    "type_, format_, value",
    [
        ("integer", None, 1),
        ("integer", "int32", 1),
        ("integer", "int64", 1),
        ("number", None, 1.1),
        ("number", "float", 1.1),
        ("string", None, "some string"),
        ("string", "password", "some password"),
        ("string", "byte", "some string"),
        ("string", "binary", b"some bytes"),
        ("string", "date", datetime.date(year=2000, month=1, day=1)),
        (
            "string",
            "date-time",
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
        ("boolean", None, True),
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
def test_database_types(engine, sessionmaker, type_, format_, value):
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
def test_database_types_default(
    engine, sessionmaker, type_, format_, default, expected_value
):
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
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)


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
def test_database_default(engine, sessionmaker):
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


@pytest.mark.integration
def test_database_many_to_one_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with a many to one object relationship
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
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
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


@pytest.mark.integration
def test_database_many_to_one_relationship_fk(engine, sessionmaker):
    """
    GIVEN specification with a schema with a many to one object relationship with a
        defined foreign key
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
                        "ref_table": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefTable"},
                                {"x-foreign-key-column": "name"},
                            ]
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
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
    assert queried_model.ref_table_name == "ref table name 1"
    assert queried_model.ref_table.name == "ref table name 1"


@pytest.mark.integration
def test_database_one_to_one_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with an one to one object relationship
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
                    "x-backref": "table",
                    "x-uselist": False,
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
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
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
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.table.id == 12


@pytest.mark.integration
def test_database_one_to_many_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with a one to many object relationship
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
                    "x-backref": "table",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_tables": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/RefTable"},
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    ref_model = model_factory(name="RefTable")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance = ref_model(id=11, name="ref table name 1")
    model_instance = model(id=12, name="table name 1", ref_tables=[ref_model_instance])
    session = sessionmaker()
    session.add(ref_model_instance)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.name == "table name 1"
    assert len(queried_model.ref_tables) == 1
    assert queried_model.ref_tables[0].id == 11
    assert queried_model.ref_tables[0].name == "ref table name 1"
    assert queried_model.ref_tables[0].table_id == 12
    assert queried_model.ref_tables[0].table.name == "table name 1"
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.id == 11
    assert queried_ref_model.name == "ref table name 1"
    assert queried_ref_model.table.id == 12


@pytest.mark.integration
def test_database_one_to_many_relationship_other_order(engine, sessionmaker):
    """
    GIVEN specification with a schema with a one to many object relationship which are
        defined in reverse order
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
                    "x-backref": "table",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_tables": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/RefTable"},
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance = ref_model(id=11, name="ref table name 1")
    model_instance = model(id=12, name="table name 1", ref_tables=[ref_model_instance])
    session = sessionmaker()
    session.add(ref_model_instance)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.ref_tables[0].id == 11


@pytest.mark.integration
def test_database_many_to_many_relationship(engine, sessionmaker):
    """
    GIVEN specification with a schema with a many to many object relationship
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
                    "x-secondary": "association",
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_tables": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/RefTable"},
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")
    ref_model = model_factory(name="RefTable")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model and ref_model
    ref_model_instance = ref_model(id=11, name="ref table name 1")
    model_instance = model(id=12, name="table name 1", ref_tables=[ref_model_instance])
    session = sessionmaker()
    session.add(ref_model_instance)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.name == "table name 1"
    assert len(queried_model.ref_tables) == 1
    assert queried_model.ref_tables[0].id == 11
    assert queried_model.ref_tables[0].name == "ref table name 1"
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.id == 11
    assert queried_ref_model.name == "ref table name 1"
    assert len(queried_ref_model.tables) == 1
    assert queried_ref_model.tables[0].id == 12
    assert queried_ref_model.tables[0].name == "table name 1"


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
def test_database_ref_all_of(engine, sessionmaker, spec):
    """
    GIVEN specification with a schema that has a $ref on a column
    WHEN schema is created and an instance is added to the session
    THEN the instance is returned when the session is queried for it.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
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
