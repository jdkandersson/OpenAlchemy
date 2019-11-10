"""Integration tests for from_dict and to_dict."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.integration
def test_to_from_dict(engine, sessionmaker):
    """
    GIVEN specification that has schema with a single property
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
                        "properties": {
                            "column": {"type": "integer", "x-primary-key": True}
                        },
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
    model_dict = {"column": 1}
    instance = model.from_dict(**model_dict)
    session = sessionmaker()
    session.add(instance)
    session.flush()
    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == model_dict


@pytest.mark.integration
def test_to_from_dict_many_to_one_relationship(engine, sessionmaker):
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
def test_to_from_dict_one_to_many_relationship(engine, sessionmaker):
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
