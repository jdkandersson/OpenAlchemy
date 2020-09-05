"""Tests for type_."""
# pylint: disable=protected-access,unused-import

import datetime
import typing  # noqa: F401

import pytest
import sqlalchemy
import typeguard
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArt = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArt = models_file.types.ColumnSchemaExtensionArtifacts


@pytest.mark.parametrize(
    "type_, format_, nullable, required, generated, value",
    [
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            1,
            id="type integer format None      value int",
        ),
        pytest.param(
            "integer",
            "int32",
            None,
            None,
            None,
            1,
            id="type integer format int32     value int",
        ),
        pytest.param(
            "integer",
            "int64",
            None,
            None,
            None,
            1,
            id="type integer format int64     value int",
        ),
        pytest.param(
            "number",
            None,
            None,
            None,
            None,
            1.0,
            id="type number  format None      value float",
        ),
        pytest.param(
            "number",
            "float",
            None,
            None,
            None,
            1.0,
            id="type number  format double    value float",
        ),
        pytest.param(
            "string",
            None,
            None,
            None,
            None,
            "value 1",
            id="type string  format None      value str",
        ),
        pytest.param(
            "string",
            "password",
            None,
            None,
            None,
            "value 1",
            id="type string  format password  value str",
        ),
        pytest.param(
            "string",
            "unsupported",
            None,
            None,
            None,
            "value 1",
            id="type string  format unsupported  value str",
        ),
        pytest.param(
            "string",
            "byte",
            None,
            None,
            None,
            "value 1",
            id="type string  format byte      value str",
        ),
        pytest.param(
            "string",
            "binary",
            None,
            None,
            None,
            b"value 1",
            id="type string  format binary    value bytes",
        ),
        pytest.param(
            "string",
            "date",
            None,
            None,
            None,
            datetime.date(year=2000, month=1, day=1),
            id="type string  format date      value datetime.date",
        ),
        pytest.param(
            "string",
            "date-time",
            None,
            None,
            None,
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
            id="type string  format date-time value datetime.datetime",
        ),
        pytest.param(
            "boolean",
            None,
            None,
            None,
            None,
            True,
            id="type boolean format None      value bool",
        ),
        # nullable
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            1,
            id="nullable None  value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            None,
            id="nullable None  value None",
        ),
        pytest.param(
            "integer",
            None,
            True,
            None,
            None,
            1,
            id="nullable True  value not None",
        ),
        pytest.param(
            "integer",
            None,
            True,
            None,
            None,
            None,
            id="nullable True  value None",
        ),
        pytest.param(
            "integer",
            None,
            False,
            None,
            None,
            1,
            id="nullable False value not None",
        ),
        # required
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            1,
            id="required None  value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            None,
            id="required None  value None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            True,
            None,
            1,
            id="required True  value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            False,
            None,
            1,
            id="required False value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            False,
            None,
            None,
            id="required False value None",
        ),
        # generated
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            1,
            id="generated None  value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            None,
            None,
            id="generated None  value None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            True,
            1,
            id="generated True  value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            False,
            1,
            id="generated False value not None",
        ),
        pytest.param(
            "integer",
            None,
            None,
            None,
            False,
            None,
            id="generated False value None",
        ),
    ],
)
@pytest.mark.models_file
def test_model_database_type_simple(
    engine, sessionmaker, type_, format_, nullable, required, generated, value
):
    """
    GIVEN simple type, format, nullable, required, generated and a value
    WHEN a specification is written for the combination and a model created and
        initialized with the value
    THEN the queried value complies with the type calculated by type_.model.
    """
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
                        "column": {
                            "type": type_,
                            "format": format_,
                            "nullable": nullable,
                        },
                    },
                    "x-tablename": "table",
                    "type": "object",
                    # Use required to implement generated
                    "required": ["column"] if required or generated else [],
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Create artifacts
    artifacts = _ColSchemaArt(
        open_api=_ColSchemaOAArt(
            type=type_, format=format_, nullable=nullable, required=required
        )
    )
    calculated_type_str = models_file._model._type.model(artifacts=artifacts)
    calculated_type = eval(calculated_type_str)  # pylint: disable=eval-used

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
    typeguard.check_type("queried_model.column", queried_model.column, calculated_type)


@pytest.mark.parametrize(
    "type_, value",
    [
        pytest.param("integer", 1, id="integer"),
        pytest.param("number", 1.0, id="number"),
        pytest.param("string", "value 1", id="string"),
        pytest.param("boolean", True, id="boolean"),
        pytest.param("object", {"key": "value"}, id="object"),
        pytest.param("array", [1], id="array"),
    ],
)
@pytest.mark.models_file
def test_model_database_type_simple_json(engine, sessionmaker, type_, value):
    """
    GIVEN JSON type
    WHEN a specification is written for the combination and a model created and
        initialized with the value
    THEN the queried value complies with the type calculated by type_.model.
    """
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
                        "column": {"type": type_, "x-json": True},
                    },
                    "x-tablename": "table",
                    "type": "object",
                    "required": ["column"],
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name="Table")

    # Create artifacts
    artifacts = _ColSchemaArt(
        open_api=_ColSchemaOAArt(type=type_, required=True),
        extension=_ColSchemaExtArt(json=True),
    )
    calculated_type_str = models_file._model._type.model(artifacts=artifacts)
    calculated_type = eval(calculated_type_str)  # pylint: disable=eval-used

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
    typeguard.check_type("queried_model.column", queried_model.column, calculated_type)


@pytest.mark.parametrize(
    "nullable, required, generated",
    [(False, None, None), (None, True, None), (None, None, True)],
    ids=[
        "nullable False value not None",
        "required False value None",
        "generated False value None",
    ],
)
@pytest.mark.models_file
def test_model_database_type_simple_nullable_fail(
    engine, sessionmaker, nullable, required, generated
):
    """
    GIVEN simple type, format, nullable, required, generated and a None value
    WHEN a specification is written for the combination and a model created and
        initialized with the value
    THEN sqlalchemy.exc.IntegrityError is raised.
    """
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
                        "column": {"type": "integer", "nullable": nullable},
                    },
                    "x-tablename": "table",
                    "type": "object",
                    # Use required to implement generated
                    "required": ["column"] if required or generated else [],
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
    model_instance = model(column=None)
    session = sessionmaker()
    session.add(model_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.flush()
