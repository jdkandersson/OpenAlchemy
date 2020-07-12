"""Tests for type_."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArt = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArt = models_file.types.ColumnSchemaExtensionArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="integer")),
            "typing.Optional[int]",
            id="plain",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="string", format="binary")),
            "typing.Optional[str]",
            id="binary",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="binary"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Optional[str]",
            id="binary json",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="string", format="date")),
            "typing.Optional[str]",
            id="date",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="date"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Optional[str]",
            id="date json",
        ),
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="string", format="date-time")),
            "typing.Optional[str]",
            id="date-time",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="string", format="date-time"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Optional[str]",
            id="date-time json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object"),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            'typing.Optional["RefModelDict"]',
            id="object",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Optional[typing.Dict]",
            id="object json",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="array"),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            'typing.Sequence["RefModelDict"]',
            id="array",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="array"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Optional[typing.Sequence]",
            id="array",
        ),
    ],
)
@pytest.mark.models_file
def test_dict(artifacts, expected_type):
    """
    GIVEN artifacts and expected type
    WHEN typed_dict is called with the artifacts
    THEN the given expected type is returned.
    """
    artifacts.nullable = True

    returned_type = models_file._model._type.typed_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.models_file
def test_dict_de_ref_none():
    """
    GIVEN object artifacts where de_ref is None
    WHEN typed_dict is called with the artifacts
    THEN MissingArgumentError is raised.
    """
    artifacts = _ColSchemaArt(
        open_api=_ColSchemaOAArt(type="object"), extension=_ColSchemaExtArt(de_ref=None)
    )

    with pytest.raises(exceptions.MissingArgumentError):
        models_file._model._type.typed_dict(artifacts=artifacts)
