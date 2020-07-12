"""Tests for type_."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts
_ColSchemaOAArt = models_file.types.ColumnSchemaOpenAPIArtifacts
_ColSchemaExtArt = models_file.types.ColumnSchemaExtensionArtifacts


@pytest.mark.parametrize(
    "nullable, required, default, expected_type",
    [
        (False, True, None, "int"),
        (False, False, None, "typing.Optional[int]"),
        (True, True, None, "typing.Optional[int]"),
        (True, False, None, "typing.Optional[int]"),
        (False, False, 1, "int"),
        (True, False, 1, "int"),
    ],
    ids=[
        "not nullable required",
        "not nullable not required",
        "nullable required",
        "nullable not required",
        "not nullable default",
        "nullable default",
    ],
)
@pytest.mark.models_file
def test_arg_init(nullable, required, default, expected_type):
    """
    GIVEN nullable and required
    WHEN arg_init is called with the nullable and required
    THEN the expected type is returned.
    """
    artifacts = _ColSchemaArt(
        open_api=_ColSchemaOAArt(
            type="integer", nullable=nullable, required=required, default=default
        )
    )

    returned_type = models_file._model._type.arg_init(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "artifacts, expected_type",
    [
        pytest.param(
            _ColSchemaArt(open_api=_ColSchemaOAArt(type="integer")), "int", id="plain"
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object"),
                extension=_ColSchemaExtArt(de_ref="RefModel"),
            ),
            '"RefModelDict"',
            id="object",
        ),
        pytest.param(
            _ColSchemaArt(
                open_api=_ColSchemaOAArt(type="object"),
                extension=_ColSchemaExtArt(json=True),
            ),
            "typing.Dict",
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
            "typing.Sequence",
            id="array json",
        ),
    ],
)
@pytest.mark.models_file
def test_arg_from_dict(artifacts, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN arg_from_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    artifacts.open_api.nullable = False
    artifacts.open_api.required = True

    returned_type = models_file._model._type.arg_from_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.models_file
def test_arg_from_dict_de_ref_none():
    """
    GIVEN object artifacts where de_ref is None
    WHEN arg_from_dict is called with the artifacts
    THEN MissingArgumentError is raised.
    """
    artifacts = _ColSchemaArt(
        open_api=_ColSchemaOAArt(type="object"), extension=_ColSchemaExtArt(de_ref=None)
    )

    with pytest.raises(exceptions.MissingArgumentError):
        models_file._model._type.arg_from_dict(artifacts=artifacts)
