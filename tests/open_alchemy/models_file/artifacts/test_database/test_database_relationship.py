"""Tests for type_."""
# pylint: disable=protected-access,unused-import

import typing  # noqa: F401

import pytest
import sqlalchemy
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import models_file
from open_alchemy import schemas


@pytest.mark.models_file
def test_model_database_type_many_to_one(engine, sessionmaker):
    """
    GIVEN spec for a many to one relationship
    WHEN spec is constructed with model factory and queried
    THEN the referenced type is a single object that is nullable and the back reference
        is an array that is not nullable.
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

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    ref_model_schemas_name, ref_model_schemas_artifacts = schemas_artifacts[0]
    assert ref_model_schemas_name == "RefTable"
    ref_model_models_artifacts = models_file._artifacts.calculate(
        artifacts=ref_model_schemas_artifacts, name="RefTable"
    )
    assert len(ref_model_models_artifacts.sqlalchemy.columns) == 3
    tables_column_artifacts = ref_model_models_artifacts.sqlalchemy.columns[2]
    assert tables_column_artifacts.name == "tables"
    calculated_backref_type_str = tables_column_artifacts.type
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_table_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_table_column_artifacts.name == "ref_table"
    calculated_type_str = ref_table_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of model and ref_model
    ref_model_instance1 = ref_model(id=11, name="ref table name 1")
    model_instance1 = model(id=12, name="table name 1", ref_table=ref_model_instance1)
    session.add(ref_model_instance1)
    session.add(model_instance1)
    session.flush()
    # Creating instance of model with None ref_model
    model_instance2 = model(id=22, name="table name 2", ref_table=None)
    session.add(model_instance2)
    session.flush()

    # Querying session
    queried_models = session.query(model).all()
    assert queried_models[0].ref_table is not None
    assert queried_models[1].ref_table is None

    # Check that returned type is correct
    assert calculated_type_str == 'typing.Optional["TRefTable"]'

    # Creating instance of ref_model without models
    ref_model_instance3 = ref_model(id=31, name="ref table name 3")
    session.add(ref_model_instance3)
    # Creating instance of ref_model without empty models
    ref_model_instance4 = ref_model(id=41, name="ref table name 4", tables=[])
    session.add(ref_model_instance4)
    # Creating instance of ref_model with single model
    ref_model_instance5 = ref_model(
        id=51, name="ref table name 5", tables=[model(id=52, name="table name 5")]
    )
    session.add(ref_model_instance5)
    session.flush()

    # Querying session
    queried_ref_models = session.query(ref_model).all()
    assert len(queried_ref_models[1].tables) == 0
    assert len(queried_ref_models[2].tables) == 0
    assert len(queried_ref_models[3].tables) == 1

    # Try constructing null for models
    with pytest.raises(TypeError):
        ref_model(id=41, name="ref table name 4", tables=None)

    assert calculated_backref_type_str == 'typing.Sequence["TTable"]'


@pytest.mark.models_file
def test_model_database_type_many_to_one_not_nullable(engine, sessionmaker):
    """
    GIVEN spec with many to one relationship that is not nullable
    WHEN models are constructed and None is passed for the object reference
    THEN sqlalchemy.exc.IntegrityError is raised.
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
                                {"nullable": False},
                            ],
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
    model_factory(name="RefTable")

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_table_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_table_column_artifacts.name == "ref_table"
    calculated_type_str = ref_table_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of model with None ref_model
    model_instance = model(id=12, name="table name 1", ref_table=None)
    session.add(model_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.flush()

    # Check that returned type is correct
    assert calculated_type_str == '"TRefTable"'


@pytest.mark.models_file
def test_model_database_type_one_to_one(engine, sessionmaker):
    """
    GIVEN spec for a one to one relationship
    WHEN spec is constructed with model factory and queried
    THEN the referenced type is a single object that is nullable and the back reference
        is an single object that is nullable.
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

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    ref_model_schemas_name, ref_model_schemas_artifacts = schemas_artifacts[0]
    assert ref_model_schemas_name == "RefTable"
    ref_model_models_artifacts = models_file._artifacts.calculate(
        artifacts=ref_model_schemas_artifacts, name="RefTable"
    )
    assert len(ref_model_models_artifacts.sqlalchemy.columns) == 3
    table_column_artifacts = ref_model_models_artifacts.sqlalchemy.columns[2]
    assert table_column_artifacts.name == "table"
    calculated_backref_type_str = table_column_artifacts.type
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_table_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_table_column_artifacts.name == "ref_table"
    calculated_type_str = ref_table_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of model and ref_model
    ref_model_instance1 = ref_model(id=11, name="ref table name 1")
    model_instance1 = model(id=12, name="table name 1", ref_table=ref_model_instance1)
    session.add(ref_model_instance1)
    session.add(model_instance1)
    session.flush()
    # Creating instance of model with None ref_model
    model_instance2 = model(id=22, name="table name 2", ref_table=None)
    session.add(model_instance2)
    session.flush()

    # Querying session
    queried_models = session.query(model).all()
    assert queried_models[0].ref_table is not None
    assert queried_models[1].ref_table is None

    # Check that returned type is correct
    assert calculated_type_str == 'typing.Optional["TRefTable"]'

    # Creating instance of ref_model without model
    ref_model_instance3 = ref_model(id=31, name="ref table name 3")
    session.add(ref_model_instance3)
    # Creating instance of ref_model with model
    ref_model_instance4 = ref_model(
        id=41, name="ref table name 4", table=model(id=42, name="table name 4")
    )
    session.add(ref_model_instance4)
    session.flush()

    # Querying session
    queried_ref_models = session.query(ref_model).all()
    assert queried_ref_models[1].table is None
    assert queried_ref_models[2].table is not None

    assert calculated_backref_type_str == 'typing.Optional["TTable"]'


@pytest.mark.models_file
def test_model_database_type_one_to_one_not_nullable(engine, sessionmaker):
    """
    GIVEN spec with one to one relationship that is not nullable
    WHEN models are constructed and None is passed for the object reference
    THEN sqlalchemy.exc.IntegrityError is raised for the relationship and not
        for the back reference which is still a single object that is nullable.
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
                    "x-uselist": False,
                },
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "ref_table": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefTable"},
                                {"nullable": False},
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

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    ref_model_schemas_name, ref_model_schemas_artifacts = schemas_artifacts[0]
    assert ref_model_schemas_name == "RefTable"
    ref_model_models_artifacts = models_file._artifacts.calculate(
        artifacts=ref_model_schemas_artifacts, name="RefTable"
    )
    assert len(ref_model_models_artifacts.sqlalchemy.columns) == 3
    table_column_artifacts = ref_model_models_artifacts.sqlalchemy.columns[2]
    assert table_column_artifacts.name == "table"
    calculated_backref_type_str = table_column_artifacts.type
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_table_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_table_column_artifacts.name == "ref_table"
    calculated_type_str = ref_table_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of ref_model without model
    ref_model_instance1 = ref_model(id=11, name="ref table name 1")
    session.add(ref_model_instance1)
    # Creating instance of ref_model with model
    ref_model_instance2 = ref_model(
        id=21, name="ref table name 2", table=model(id=22, name="table name 2")
    )
    session.add(ref_model_instance2)
    session.flush()

    # Querying session
    queried_ref_models = session.query(ref_model).all()
    assert queried_ref_models[0].table is None
    assert queried_ref_models[1].table is not None

    assert calculated_backref_type_str == 'typing.Optional["TTable"]'

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of model with None ref_model
    model_instance = model(id=32, name="table name 3", ref_table=None)
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.flush()

    # Check that returned type is correct
    assert calculated_type_str == '"TRefTable"'


@pytest.mark.models_file
def test_model_database_type_one_to_many(engine, sessionmaker):
    """
    GIVEN spec for a one to many relationship
    WHEN spec is constructed with model factory and queried
    THEN the referenced type is an array that is not nullable and the back reference
        is an object that is nullable.
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

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    ref_model_schemas_name, ref_model_schemas_artifacts = schemas_artifacts[0]
    assert ref_model_schemas_name == "RefTable"
    ref_model_models_artifacts = models_file._artifacts.calculate(
        artifacts=ref_model_schemas_artifacts, name="RefTable"
    )
    assert len(ref_model_models_artifacts.sqlalchemy.columns) == 3
    table_column_artifacts = ref_model_models_artifacts.sqlalchemy.columns[2]
    assert table_column_artifacts.name == "table"
    calculated_backref_type_str = table_column_artifacts.type
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_tables_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_tables_column_artifacts.name == "ref_tables"
    calculated_type_str = ref_tables_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of model without ref_models
    model_instance1 = model(id=11, name="ref table name 1")
    session.add(model_instance1)
    # Creating instance of model without empty ref_models
    model_instance2 = model(id=21, name="ref table name 2", ref_tables=[])
    session.add(model_instance2)
    # Creating instance of model with single ref_model
    model_instance3 = model(
        id=31,
        name="ref table name 3",
        ref_tables=[ref_model(id=32, name="table name 3")],
    )
    session.add(model_instance3)
    session.flush()

    # Querying session
    queried_models = session.query(model).all()
    assert len(queried_models[0].ref_tables) == 0
    assert len(queried_models[1].ref_tables) == 0
    assert len(queried_models[2].ref_tables) == 1

    # Try constructing null for models
    with pytest.raises(TypeError):
        model(id=41, name="ref table name 4", ref_tables=None)

    assert calculated_type_str == 'typing.Sequence["TRefTable"]'

    # Creating instance of ref_model with model
    ref_model_instance5 = ref_model(
        id=51, name="ref table name 5", table=model(id=52, name="table name 5")
    )
    session.add(ref_model_instance5)
    # Creating instance of ref_model with None model
    ref_model_instance6 = ref_model(id=61, name="ref table name 6", table=None)
    session.add(ref_model_instance6)
    session.flush()

    # Querying session
    queried_models = session.query(ref_model).all()
    assert queried_models[1].table is not None
    assert queried_models[2].table is None

    assert calculated_backref_type_str == 'typing.Optional["TTable"]'


@pytest.mark.models_file
def test_model_database_type_many_to_many(engine, sessionmaker):
    """
    GIVEN spec for a many to many relationship
    WHEN spec is constructed with model factory and queried
    THEN the referenced and back reference type is an array that is not nullable.
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
                    "x-secondary": "association",
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

    # Calculate the expected type
    schemas_artifacts = schemas.artifacts.get_from_schemas(
        schemas=spec["components"]["schemas"], stay_within_model=False
    )
    assert len(schemas_artifacts) == 2
    ref_model_schemas_name, ref_model_schemas_artifacts = schemas_artifacts[0]
    assert ref_model_schemas_name == "RefTable"
    ref_model_models_artifacts = models_file._artifacts.calculate(
        artifacts=ref_model_schemas_artifacts, name="RefTable"
    )
    assert len(ref_model_models_artifacts.sqlalchemy.columns) == 3
    tables_column_artifacts = ref_model_models_artifacts.sqlalchemy.columns[2]
    assert tables_column_artifacts.name == "tables"
    calculated_backref_type_str = tables_column_artifacts.type
    model_schemas_name, model_schemas_artifacts = schemas_artifacts[1]
    assert model_schemas_name == "Table"
    model_models_artifacts = models_file._artifacts.calculate(
        artifacts=model_schemas_artifacts, name="Table"
    )
    assert len(model_models_artifacts.sqlalchemy.columns) == 3
    ref_tables_column_artifacts = model_models_artifacts.sqlalchemy.columns[2]
    assert ref_tables_column_artifacts.name == "ref_tables"
    calculated_type_str = ref_tables_column_artifacts.type

    # Creating models
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Creating instance of model without ref_models
    model_instance1 = model(id=11, name="ref table name 1")
    session.add(model_instance1)
    # Creating instance of model without empty ref_models
    model_instance2 = model(id=21, name="ref table name 2", ref_tables=[])
    session.add(model_instance2)
    # Creating instance of model with single ref_model
    model_instance3 = model(
        id=31,
        name="ref table name 3",
        ref_tables=[ref_model(id=32, name="table name 3")],
    )
    session.add(model_instance3)
    session.flush()

    # Querying session
    queried_models = session.query(model).all()
    assert len(queried_models[0].ref_tables) == 0
    assert len(queried_models[1].ref_tables) == 0
    assert len(queried_models[2].ref_tables) == 1

    # Try constructing null for models
    with pytest.raises(TypeError):
        model(id=41, name="ref table name 4", ref_tables=None)

    assert calculated_type_str == 'typing.Sequence["TRefTable"]'

    # Creating instance of ref_model without models
    ref_model_instance5 = ref_model(id=51, name="ref table name 5")
    session.add(ref_model_instance5)
    # Creating instance of ref_model without empty models
    ref_model_instance6 = ref_model(id=61, name="ref table name 6", tables=[])
    session.add(ref_model_instance6)
    # Creating instance of ref_model with single model
    ref_model_instance7 = ref_model(
        id=71, name="ref table name 7", tables=[model(id=72, name="table name 7")]
    )
    session.add(ref_model_instance7)
    session.flush()

    # Querying session
    queried_ref_models = session.query(ref_model).all()
    assert len(queried_ref_models[1].tables) == 0
    assert len(queried_ref_models[2].tables) == 0
    assert len(queried_ref_models[3].tables) == 1

    # Try constructing null for models
    with pytest.raises(TypeError):
        ref_model(id=81, name="ref table name 8", tables=None)

    assert calculated_backref_type_str == 'typing.Sequence["TTable"]'
