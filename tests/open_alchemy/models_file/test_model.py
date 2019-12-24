"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "type_, format_, nullable, required, expected_type",
    [
        ("integer", None, False, None, "int"),
        ("integer", "int32", False, None, "int"),
        ("integer", "int64", False, None, "int"),
        ("number", None, False, None, "float"),
        ("number", "float", False, None, "float"),
        ("string", None, False, None, "str"),
        ("string", "password", False, None, "str"),
        ("string", "byte", False, None, "str"),
        ("string", "binary", False, None, "bytes"),
        ("string", "date", False, None, "datetime.date"),
        ("string", "date-time", False, None, "datetime.datetime"),
        ("boolean", None, False, None, "bool"),
        ("integer", None, None, None, "typing.Optional[int]"),
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
        "nullable and required None",
    ],
)
@pytest.mark.models_file
def test_calculate_type(type_, format_, nullable, required, expected_type):
    """
    GIVEN type, format, nullable and required
    WHEN _calculate_type is called with the type, format, nullable and required
    THEN the expected type is returned.
    """
    returned_type = models_file._model._calculate_type(
        type_=type_, format_=format_, nullable=nullable, required=required
    )

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
def test_generate(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN generate is called with the artifacts
    THEN the source code for the model class is returned.
    """
    source = models_file._model.generate(artifacts=artifacts)

    assert source == expected_source
