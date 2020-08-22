"""Tests for type_."""
# pylint: disable=protected-access


import pytest

from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArt = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArt = models_file.types.ColumnSchemaExtensionArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="integer", nullable=False)),
            "int",
            id="integer no format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer", format="int32", nullable=False)
            ),
            "int",
            id="integer int32 format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer", format="int64", nullable=False)
            ),
            "int",
            id="integer int64 format",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="number", nullable=False)),
            "float",
            id="number no format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="number", format="float", nullable=False)
            ),
            "float",
            id="number float format",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="string", nullable=False)),
            "str",
            id="string no format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="password", nullable=False
                )
            ),
            "str",
            id="string password format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="unsupported", nullable=False
                )
            ),
            "str",
            id="string unsupported format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="byte", nullable=False)
            ),
            "str",
            id="string byte format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="binary", nullable=False)
            ),
            "bytes",
            id="string binary format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="date", nullable=False)
            ),
            "datetime.date",
            id="string date format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="date-time", nullable=False
                )
            ),
            "datetime.datetime",
            id="string date-time format",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="boolean", nullable=False)),
            "bool",
            id="boolean no format",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object", nullable=False),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            '"TRefModel"',
            id="object",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="object", nullable=False, default="value 1"
                ),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            '"TRefModel"',
            id="object defult",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="array"),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            'typing.Sequence["TRefModel"]',
            id="array",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="array", default="value 1"),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            'typing.Sequence["TRefModel"]',
            id="array default",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="integer")),
            "typing.Optional[int]",
            id="nullable and required None",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="integer", required=True)),
            "int",
            id="nullable None required True",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer"),
                extension=_ColSchemaExtArt(generated=True),
            ),
            "int",
            id="nullable None generated True",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer"),
                extension=_ColSchemaExtArt(generated=False),
            ),
            "typing.Optional[int]",
            id="nullable None generated False",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer", default=1),
                extension=_ColSchemaExtArt(generated=False),
            ),
            "int",
            id="nullable None default given",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="integer", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "int",
            id="integer json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="number", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "float",
            id="number json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="password", nullable=False
                ),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="password string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="unsupported", nullable=False
                ),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="unsupported string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="byte", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="byte string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="binary", nullable=False
                ),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="binary string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="date", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="date string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(
                    type="string", format="date-time", nullable=False
                ),
                extension=_ColSchemaExtArt(json=True),
            ),
            "str",
            id="date-time string json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="boolean", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "bool",
            id="date-time boolean json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Dict",
            id="date-time object json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="array", nullable=False),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Sequence",
            id="date-time array json",
        ),
    ],
)
@pytest.mark.models_file
def test_model(artifacts, expected_type):
    """
    GIVEN artifacts
    WHEN model is called with the artifacts
    THEN the expected type is returned.
    """
    returned_type = models_file._model._type.model(artifacts=artifacts)

    assert returned_type == expected_type
