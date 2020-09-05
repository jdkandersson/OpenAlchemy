"""Integration tests against database for relationships."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.integration
def test_many_to_one(engine, sessionmaker):
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
def test_many_to_one_backref(engine, sessionmaker):
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
    ref_model_instance = ref_model(
        id=11, name="ref table name 1", tables=[model(id=12, name="table name 1")]
    )
    session = sessionmaker()
    session.add(ref_model_instance)
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
def test_many_to_one_relationship_fk(engine, sessionmaker):
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
def test_one_to_one(engine, sessionmaker):
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
def test_one_to_many(engine, sessionmaker):
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
    assert queried_model.ref_tables[0].table_ref_tables_id == 12
    assert queried_model.ref_tables[0].table.name == "table name 1"
    queried_ref_model = session.query(ref_model).first()
    assert queried_ref_model.id == 11
    assert queried_ref_model.name == "ref table name 1"
    assert queried_ref_model.table.id == 12


@pytest.mark.integration
def test_one_to_many_relationship_kwargs(engine, sessionmaker):
    """
    GIVEN specification with a schema with a one to many object relationship with kwargs
    WHEN schema is created, values inserted in both tables and queried
    THEN the data is returned as specified by kwargs.
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
                            "items": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefTable"},
                                    {
                                        "x-kwargs": {
                                            "order_by": "desc(RefTable.name)",
                                            "lazy": "dynamic",
                                        }
                                    },
                                ]
                            },
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
    ref_model_instance1 = ref_model(id=11, name="ref table name 1")
    ref_model_instance2 = ref_model(id=21, name="ref table name 2")
    model_instance = model(
        id=12,
        name="table name 1",
        ref_tables=[ref_model_instance1, ref_model_instance2],
    )
    session = sessionmaker()
    session.add(ref_model_instance1)
    session.add(ref_model_instance2)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    ref_tables = list(ref_table.name for ref_table in queried_model.ref_tables)
    assert ref_tables == ["ref table name 2", "ref table name 1"]


@pytest.mark.integration
def test_one_to_many_relationship_other_order(engine, sessionmaker):
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
def test_many_to_many(engine, sessionmaker):
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
def test_ref_all_of(engine, sessionmaker, spec):
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


@pytest.mark.integration
def test_multiple(engine, sessionmaker):
    """
    GIVEN specification with a schema with multiple relationships pointing to the same
        table
    WHEN schema is created, values inserted in both tables and queried
    THEN the data is returned as it was inserted with the correct foreign key.
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
                    "type": "object",
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table_first": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefTable"},
                                {
                                    "x-kwargs": {
                                        "foreign_keys": "Table.ref_table_first_id"
                                    }
                                },
                            ]
                        },
                        "ref_table_second": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefTable"},
                                {
                                    "x-kwargs": {
                                        "foreign_keys": "Table.ref_table_second_id"
                                    }
                                },
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
    ref_model_instance_first = ref_model(id=11, name="ref table name 1")
    ref_model_instance_second = ref_model(id=21, name="ref table name 2")
    model_instance = model(
        id=12,
        name="table name 1",
        ref_table_first=ref_model_instance_first,
        ref_table_second=ref_model_instance_second,
    )
    session = sessionmaker()
    session.add(ref_model_instance_first)
    session.add(ref_model_instance_second)
    session.add(model_instance)
    session.flush()

    # Querying session
    queried_model = session.query(model).first()
    assert queried_model.id == 12
    assert queried_model.name == "table name 1"
    assert queried_model.ref_table_first_id == 11
    assert queried_model.ref_table_first.id == 11
    assert queried_model.ref_table_second_id == 21
    assert queried_model.ref_table_second.id == 21
    assert queried_model.ref_table_first.name == "ref table name 1"
    assert queried_model.ref_table_second.name == "ref table name 2"
