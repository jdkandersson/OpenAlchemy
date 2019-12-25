"""Tests for type_."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "type_, format_, nullable, required, de_ref, expected_type",
    [
        ("integer", None, False, None, None, "int"),
        ("integer", "int32", False, None, None, "int"),
        ("integer", "int64", False, None, None, "int"),
        ("number", None, False, None, None, "float"),
        ("number", "float", False, None, None, "float"),
        ("string", None, False, None, None, "str"),
        ("string", "password", False, None, None, "str"),
        ("string", "byte", False, None, None, "str"),
        ("string", "binary", False, None, None, "bytes"),
        ("string", "date", False, None, None, "datetime.date"),
        ("string", "date-time", False, None, None, "datetime.datetime"),
        ("boolean", None, False, None, None, "bool"),
        ("object", None, False, None, "RefModel", '"RefModel"'),
        ("array", None, None, None, "RefModel", 'typing.Sequence["RefModel"]'),
        ("integer", None, None, None, None, "typing.Optional[int]"),
    ],
    ids=[
        "integer no format",
        "integer int32 format",
        "integer int64 format",
        "number no format",
        "number float format",
        "string no format",
        "string password format",
        "string byte format",
        "string binary format",
        "string date format",
        "string date-time format",
        "boolean no format",
        "object",
        "array",
        "nullable and required None",
    ],
)
@pytest.mark.models_file
def test_model(type_, format_, nullable, required, de_ref, expected_type):
    """
    GIVEN type, format, nullable and required
    WHEN model is called with the type, format, nullable and required
    THEN the expected type is returned.
    """
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_, format=format_, nullable=nullable, required=required, de_ref=de_ref
    )

    returned_type = models_file._model._type.model(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", "int"),
        ("object", '"RefModelDict"'),
        ("array", 'typing.Sequence["RefModelDict"]'),
    ],
    ids=["plain", "object", "array"],
)
@pytest.mark.models_file
def test_dict(type_, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN typed_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_, nullable=False, de_ref="RefModel"
    )

    returned_type = models_file._model._type.typed_dict(artifacts=artifacts)

    assert returned_type == expected_type
