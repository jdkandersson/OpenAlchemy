"""Tests for artifacts."""
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
    artifacts = models_file._model._artifacts.gather_column_artifacts(
        schema=schema, required=required
    )

    assert artifacts == expected_artifacts


@pytest.mark.models_file
def test_calculate_name():
    """
    GIVEN name
    WHEN calculate is called with the name
    THEN the name is added to the artifacts.
    """
    schema = {"properties": {}}
    name = "Model"

    artifacts = models_file._model._artifacts.calculate(schema=schema, name=name)

    assert artifacts.name == name


@pytest.mark.parametrize(
    "schema, expected_columns",
    [
        ({"properties": {}}, []),
        (
            {"properties": {"column_1": {"type": "integer"}}},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
        (
            {
                "properties": {
                    "column_1": {"type": "integer"},
                    "column_2": {"type": "string"},
                }
            },
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                ),
                models_file.types.ColumnArtifacts(
                    name="column_2", type="typing.Optional[str]"
                ),
            ],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": ["column_1"]},
            [models_file.types.ColumnArtifacts(name="column_1", type="int")],
        ),
        (
            {"properties": {"column_1": {"type": "integer"}}, "required": []},
            [
                models_file.types.ColumnArtifacts(
                    name="column_1", type="typing.Optional[int]"
                )
            ],
        ),
    ],
    ids=["empty", "single", "multiple", "single in required", "single not in required"],
)
@pytest.mark.models_file
def test_calculate_column(schema, expected_columns):
    """
    GIVEN schema
    WHEN calculate is called with the schema
    THEN the artifacts for the columns are gathered.
    """
    artifacts = models_file._model._artifacts.calculate(schema=schema, name="Model")

    assert artifacts.columns == expected_columns
