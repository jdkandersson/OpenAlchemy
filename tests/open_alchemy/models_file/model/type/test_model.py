"""Tests for type_."""
# pylint: disable=protected-access


import pytest

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
