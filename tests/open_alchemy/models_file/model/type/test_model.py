"""Tests for type_."""
# pylint: disable=protected-access,unused-import

import datetime
import typing  # noqa: F401

import pytest
import sqlalchemy
import typeguard
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import exceptions
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _ColSchemaArt(type="integer", nullable=False),
            "int",
            id="integer no format",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", format="int32", nullable=False),
            "int",
            id="integer int32 format",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", format="int64", nullable=False),
            "int",
            id="integer int64 format",
        ),
        pytest.param(
            _ColSchemaArt(type="number", nullable=False),
            "float",
            id="number no format",
        ),
        pytest.param(
            _ColSchemaArt(type="number", format="float", nullable=False),
            "float",
            id="number float format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", nullable=False), "str", id="string no format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="password", nullable=False),
            "str",
            id="string password format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="byte", nullable=False),
            "str",
            id="string byte format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="binary", nullable=False),
            "bytes",
            id="string binary format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="date", nullable=False),
            "datetime.date",
            id="string date format",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="date-time", nullable=False),
            "datetime.datetime",
            id="string date-time format",
        ),
        pytest.param(
            _ColSchemaArt(type="boolean", nullable=False),
            "bool",
            id="boolean no format",
        ),
        pytest.param(
            _ColSchemaArt(type="object", nullable=False, de_ref="RefModel"),
            '"TRefModel"',
            id="object",
        ),
        pytest.param(
            _ColSchemaArt(
                type="object", nullable=False, de_ref="RefModel", default="value 1"
            ),
            '"TRefModel"',
            id="object defult",
        ),
        pytest.param(
            _ColSchemaArt(type="array", de_ref="RefModel"),
            'typing.Sequence["TRefModel"]',
            id="array",
        ),
        pytest.param(
            _ColSchemaArt(type="array", de_ref="RefModel", default="value 1"),
            'typing.Sequence["TRefModel"]',
            id="array default",
        ),
        pytest.param(
            _ColSchemaArt(type="integer"),
            "typing.Optional[int]",
            id="nullable and required None",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", required=True),
            "int",
            id="nullable None required True",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", generated=True),
            "int",
            id="nullable None generated True",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", generated=False),
            "typing.Optional[int]",
            id="nullable None generated False",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", generated=False, default=1),
            "int",
            id="nullable None default given",
        ),
        pytest.param(
            _ColSchemaArt(type="integer", json=True, nullable=False),
            "int",
            id="integer json",
        ),
        pytest.param(
            _ColSchemaArt(type="number", json=True, nullable=False),
            "float",
            id="number json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", json=True, nullable=False),
            "str",
            id="string json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="password", json=True, nullable=False),
            "str",
            id="password string json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="byte", json=True, nullable=False),
            "str",
            id="byte string json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="binary", json=True, nullable=False),
            "str",
            id="binary string json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="date", json=True, nullable=False),
            "str",
            id="date string json",
        ),
        pytest.param(
            _ColSchemaArt(type="string", format="date-time", json=True, nullable=False),
            "str",
            id="date-time string json",
        ),
        pytest.param(
            _ColSchemaArt(type="boolean", json=True, nullable=False),
            "bool",
            id="date-time boolean json",
        ),
        pytest.param(
            _ColSchemaArt(type="object", json=True, nullable=False),
            "typing.Dict",
            id="date-time object json",
        ),
        pytest.param(
            _ColSchemaArt(type="array", json=True, nullable=False),
            "typing.Sequence",
            id="date-time array json",
        ),
    ],
)
@pytest.mark.models_file
@pytest.mark.only_this
def test_model(artifacts, expected_type):
    """
    GIVEN artifacts
    WHEN model is called with the artifacts
    THEN the expected type is returned.
    """
    returned_type = models_file._model._type.model(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "type_, format_, nullable, required, generated, value",
    [
        ("integer", None, None, None, None, 1),
        ("integer", "int32", None, None, None, 1),
        ("integer", "int64", None, None, None, 1),
        ("number", None, None, None, None, 1.0),
        ("number", "float", None, None, None, 1.0),
        ("string", None, None, None, None, "value 1"),
        ("string", "password", None, None, None, "value 1"),
        ("string", "byte", None, None, None, "value 1"),
        ("string", "binary", None, None, None, b"value 1"),
        ("string", "date", None, None, None, datetime.date(year=2000, month=1, day=1)),
        (
            "string",
            "date-time",
            None,
            None,
            None,
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
        ("boolean", None, None, None, None, True),
        # nullable
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, True, None, None, 1),
        ("integer", None, True, None, None, None),
        ("integer", None, False, None, None, 1),
        # required
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, None, True, None, 1),
        ("integer", None, None, False, None, 1),
        ("integer", None, None, False, None, None),
        # generated
        ("integer", None, None, None, None, 1),
        ("integer", None, None, None, None, None),
        ("integer", None, None, None, True, 1),
        ("integer", None, None, None, False, 1),
        ("integer", None, None, None, False, None),
    ],
    ids=[
        "type integer format None      value int",
        "type integer format int32     value int",
        "type integer format int64     value int",
        "type number  format None      value float",
        "type number  format double    value float",
        "type string  format None      value str",
        "type string  format password  value str",
        "type string  format byte      value str",
        "type string  format binary    value bytes",
        "type string  format date      value datetime.date",
        "type string  format date-time value datetime.datetime",
        "type boolean format None      value bool",
        "nullable None  value not None",
        "nullable None  value None",
        "nullable True  value not None",
        "nullable True  value None",
        "nullable False value not None",
        "required None  value not None",
        "required None  value None",
        "required True  value not None",
        "required False value not None",
        "required False value None",
        "generated None  value not None",
        "generated None  value None",
        "generated True  value not None",
        "generated False value not None",
        "generated False value None",
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
        type=type_, format=format_, nullable=nullable, required=required
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
