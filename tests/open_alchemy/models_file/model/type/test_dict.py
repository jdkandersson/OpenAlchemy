"""Tests for type_."""
# pylint: disable=protected-access

import pytest

from open_alchemy import exceptions
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts


@pytest.mark.parametrize(
    "type_, format_, expected_type",
    [
        pytest.param("integer", None, "typing.Optional[int]", id="plain"),
        pytest.param("string", "binary", "typing.Optional[str]", id="binary"),
        pytest.param("string", "date", "typing.Optional[str]", id="date"),
        pytest.param("string", "date-time", "typing.Optional[str]", id="date-time"),
        pytest.param("object", None, 'typing.Optional["RefModelDict"]', id="object"),
        pytest.param("array", None, 'typing.Sequence["RefModelDict"]', id="array"),
    ],
)
@pytest.mark.models_file
def test_dict(type_, format_, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN typed_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    artifacts = _ColSchemaArt(
        type=type_, format=format_, nullable=True, de_ref="RefModel"
    )

    returned_type = models_file._model._type.typed_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.models_file
def test_dict_de_ref_none():
    """
    GIVEN object artifacts where de_ref is None
    WHEN typed_dict is called with the artifacts
    THEN MissingArgumentError is raised.
    """
    artifacts = _ColSchemaArt(type="object", de_ref=None)

    with pytest.raises(exceptions.MissingArgumentError):
        models_file._model._type.typed_dict(artifacts=artifacts)
