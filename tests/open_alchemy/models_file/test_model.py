"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "schema, required, expected_artifacts",
    [
        (
            {"type": "type 1"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1"),
        ),
        (
            {"type": "type 1", "format": "format 1"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1", format="format 1"),
        ),
        (
            {"type": "type 1", "nullable": True},
            None,
            models_file.types.ColumnSchemaArtifacts(type="type 1", nullable=True),
        ),
        (
            {"type": "object", "x-de-$ref": "RefModel"},
            None,
            models_file.types.ColumnSchemaArtifacts(type="object", de_ref="RefModel"),
        ),
        (
            {"type": "array", "items": {"x-de-$ref": "RefModel"}},
            None,
            models_file.types.ColumnSchemaArtifacts(type="array", de_ref="RefModel"),
        ),
        (
            {"type": "type 1"},
            True,
            models_file.types.ColumnSchemaArtifacts(type="type 1", required=True),
        ),
    ],
    ids=[
        "type only",
        "type with format",
        "type with nullable",
        "object",
        "array",
        "required given",
    ],
)
@pytest.mark.models_file
def test_gather_column_artifacts(schema, required, expected_artifacts):
    """
    GIVEN schema and required
    WHEN gather_column_artifacts is called with the schema and required
    THEN the given expected artifacts are returned.
    """
    artifacts = models_file._model.gather_column_artifacts(
        schema=schema, required=required
    )

    assert artifacts == expected_artifacts


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
        ("object", None, False, None, "RefModel", "RefModel"),
        ("array", None, False, None, "RefModel", "typing.Sequence[RefModel]"),
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
def test_calculate_type(type_, format_, nullable, required, de_ref, expected_type):
    """
    GIVEN type, format, nullable and required
    WHEN _calculate_type is called with the type, format, nullable and required
    THEN the expected type is returned.
    """
    artifacts = models_file.types.ColumnSchemaArtifacts(
        type=type_, format=format_, nullable=nullable, required=required, de_ref=de_ref
    )

    returned_type = models_file._model._calculate_type(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.ModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
            ),
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    column_1: type_1''',
        ),
        (
            models_file.types.ModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
            ),
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    column_1: type_1
    column_2: type_2''',
        ),
    ],
    ids=["single column", "multiple column"],
)
@pytest.mark.models_file
def test_generate_source(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN generate_source is called with the artifacts
    THEN the source code for the model class is returned.
    """
    source = models_file._model.generate_source(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "schema, expected_source",
    [
        (
            {"properties": {"id": {"type": "integer"}}},
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    id: typing.Optional[int]''',
        ),
        (
            {"properties": {"id": {"type": "integer"}}, "required": ["id"]},
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    id: int''',
        ),
        (
            {"properties": {"id": {"type": "integer"}}, "required": []},
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    id: typing.Optional[int]''',
        ),
    ],
    ids=["single property", "single required property", "single not required property"],
)
@pytest.mark.models_file
def test_generate(schema, expected_source):
    """
    GIVEN schema and name
    WHEN generate is called with the schema and name
    THEN the model source code is returned.
    """
    source = models_file._model.generate(schema=schema, name="Model")

    assert source == expected_source
