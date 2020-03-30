"""Tests for schema helpers."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        ({}, {}, False),
        ({"x-tablename": "table 1"}, {}, True),
        ({"x-inherits": "Schema1"}, {}, True),
        (
            {"$ref": "#/components/schemas/Schema1"},
            {"Schema1": {"x-tablename": "table 1"}},
            False,
        ),
        ({"allOf": []}, {}, False),
        (
            {"allOf": [{"$ref": "#/components/schemas/Schema1"}]},
            {"Schema1": {"x-tablename": "table 1"}},
            False,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/Schema1"}, {"key": "value"}]},
            {"Schema1": {"x-tablename": "table 1"}},
            True,
        ),
    ],
    ids=[
        "empty",
        "x-tablename",
        "x-inherits",
        "x-tablename $ref only",
        "allOf empty",
        "allOf x-tablename",
        "allOf x-tablename with additional",
    ],
)
@pytest.mark.helper
def test_constractable(schema, schemas, expected_result):
    """
    GIVEN schema and schemas
    WHEN constractable is called with the schema and schemas
    THEN the expected constructable is returned.
    """
    result = helpers.schema.constructable(schema=schema, schemas=schemas)

    assert result == expected_result


@pytest.mark.helper
def test_constractable_remote(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN schema with remote $ref with x-tablename
    WHEN constractable is called with the schema
    THEN True is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Table": {"x-tablename": "table 1"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    schema = {"$ref": "remote.json#/Table"}

    result = helpers.schema.constructable(schema=schema, schemas={})

    assert result is True
