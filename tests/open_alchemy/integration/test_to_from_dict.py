"""Integration tests for from_dict and to_dict."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.parametrize(
    "column_schema, value",
    [
        ({"type": "integer", "x-primary-key": True}, 1),
        (
            {"type": "string", "format": "binary", "x-primary-key": True},
            "some binary files",
        ),
        ({"type": "string", "format": "date", "x-primary-key": True}, "2000-01-01"),
        (
            {"type": "string", "format": "date-time", "x-primary-key": True},
            "2000-01-01T01:01:01",
        ),
    ],
    ids=["integer", "binary", "date", "date-time"],
)
@pytest.mark.integration
def test_basic_types(engine, sessionmaker, column_schema, value):
    """
    GIVEN specification that has schema with a basic type property
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "Table": {
                        "properties": {"column": column_schema},
                        "x-tablename": "table",
                        "type": "object",
                    }
                }
            }
        },
    )
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"column": value}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_many_to_one(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a many to one relationship
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "ref_table": {"$ref": "#/components/schemas/RefTable"},
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
    )
    model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_table": {"id": 12}}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_many_to_one_read_only(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a many to one relationship with read
        only on child
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned with readOnly
        property.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "tables": {
                                "type": "array",
                                "readOnly": True,
                                "items": {
                                    "type": "object",
                                    "properties": {"id": {"type": "integer"}},
                                },
                            },
                        },
                        "x-tablename": "ref_table",
                        "x-backref": "tables",
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "ref_table": {"$ref": "#/components/schemas/RefTable"},
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
    )
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_table": {"id": 12}}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_ref_instance = session.query(ref_model).first()
    assert queried_ref_instance.to_dict() == {"id": 12, "tables": [{"id": 11}]}


@pytest.mark.integration
def test_to_from_dict_one_to_many(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a one to many relationship
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
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
        },
    )
    model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_tables": [{"id": 12}]}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_one_to_many_read_only(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a one to many relationship with read
        only on the child
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary with read only value is
        returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "table": {
                                "readOnly": True,
                                "type": "object",
                                "properties": {"id": {"type": "integer"}},
                            },
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                        "x-backref": "table",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
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
        },
    )
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_tables": [{"id": 12}]}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_ref_instance = session.query(ref_model).first()
    assert queried_ref_instance.to_dict() == {"id": 12, "table": {"id": 11}}


@pytest.mark.integration
def test_to_from_dict_one_to_many_fk_def(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a one to many relationship with defined
        foreign key
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called on the child the parent foreign key is returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "table_ref_tables_id": {
                                "type": "integer",
                                "x-foreign-key": "table.id",
                            },
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
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
        },
    )
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_tables": [{"id": 12}]}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_ref_instance = session.query(ref_model).first()
    assert queried_ref_instance.to_dict() == {"id": 12, "table_ref_tables_id": 11}


@pytest.mark.integration
def test_to_from_dict_one_to_one_read_only(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a one to one relationship with read
        only on child
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned with readOnly
        property.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "table": {
                                "readOnly": True,
                                "type": "object",
                                "properties": {"id": {"type": "integer"}},
                            },
                        },
                        "x-tablename": "ref_table",
                        "x-backref": "table",
                        "x-uselist": False,
                        "type": "object",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "ref_table": {"$ref": "#/components/schemas/RefTable"},
                        },
                        "x-tablename": "table",
                        "type": "object",
                    },
                }
            }
        },
    )
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_table": {"id": 12}}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_ref_instance = session.query(ref_model).first()
    assert queried_ref_instance.to_dict() == {"id": 12, "table": {"id": 11}}


@pytest.mark.integration
def test_to_from_dict_many_to_many(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a many to many relationship
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary is returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                        "x-secondary": "association",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
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
        },
    )
    model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_tables": [{"id": 12}]}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_many_to_many_read_only(engine, sessionmaker):
    """
    GIVEN specification that has a schema with a many to many relationship with read
        only on the child
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary with read only value is
        returned.
    """
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(
        base=base,
        spec={
            "components": {
                "schemas": {
                    "RefTable": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
                            "tables": {
                                "readOnly": True,
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {"id": {"type": "integer"}},
                                },
                            },
                        },
                        "x-tablename": "ref_table",
                        "type": "object",
                        "x-backref": "tables",
                        "x-secondary": "association",
                    },
                    "Table": {
                        "properties": {
                            "id": {"type": "integer", "x-primary-key": True},
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
        },
    )
    ref_model = model_factory(name="RefTable")
    model = model_factory(name="Table")
    # Creating models
    base.metadata.create_all(engine)

    # Constructing and turning back to dictionary
    model_dict = {"id": 11, "ref_tables": [{"id": 12}]}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_ref_instance = session.query(ref_model).first()
    assert queried_ref_instance.to_dict() == {"id": 12, "tables": [{"id": 11}]}


@pytest.mark.integration
def test_inheritance(engine, sessionmaker):
    """
    GIVEN specification with a schema with inheritance
    WHEN model is defined based on schema and constructed using from_dict
    THEN when to_dict is called the construction dictionary contains parent values.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Employee": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "x-tablename": "employee",
                    "type": "object",
                    "x-kwargs": {
                        "__mapper_args__": {
                            "polymorphic_on": "type",
                            "polymorphic_identity": "employee",
                        }
                    },
                },
                "Manager": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {"manager_data": {"type": "string"}},
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "manager"}
                            },
                        },
                    ]
                },
                "Engineer": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {"engineer_info": {"type": "string"}},
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "engineer"}
                            },
                        },
                    ]
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    employee = model_factory(name="Employee")
    manager = model_factory(name="Manager")

    # Creating models
    base.metadata.create_all(engine)

    # Creating instance of models
    employee_dict = {"id": 1, "name": "employee 1", "type": "employee"}
    manager_dict = {
        "id": 2,
        "name": "employee 2",
        "type": "manager",
        "manager_data": "manager data 2",
    }
    employee_instance = employee.from_dict(**employee_dict)
    manager_instance = manager.from_dict(**manager_dict)
    session = sessionmaker()
    session.add(employee_instance)
    session.add(manager_instance)
    session.flush()

    queried_employee = session.query(employee).first()
    assert queried_employee.to_dict() == employee_dict
    queried_manager = session.query(manager).first()
    assert queried_manager.to_dict() == manager_dict
