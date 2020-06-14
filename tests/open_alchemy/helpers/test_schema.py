"""Tests for schema helpers."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        ({}, {}, False),
        ({"x-tablename": "table 1"}, {}, True),
        ({"x-inherits": "Schema1"}, {}, True),
        ({"x-inherits": True}, {}, True),
        ({"x-inherits": False}, {}, False),
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
        "x-inherits string",
        "x-inherits bool true",
        "x-inherits bool false",
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


@pytest.mark.parametrize(
    "schema, expected_result",
    [
        ({}, None),
        ({"x-inherits": True}, True),
        ({"x-inherits": False}, False),
        ({"x-inherits": ""}, True),
        ({"x-inherits": "Parent"}, True),
    ],
    ids=["missing", "bool true", "bool false", "string empty", "string not empty"],
)
@pytest.mark.helper
def test_inherits(schema, expected_result):
    """
    GIVEN schema and expected result
    WHEN inherits is called with the schema
    THEN the expected result is returned.
    """
    result = helpers.schema.inherits(schema=schema, schemas={})

    assert result == expected_result


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"key": "value"}, {}),
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"key": "value"}}),
        ({"allOf": [{"key": "value"}]}, {}),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
        ),
    ],
    ids=["plain", "$ref", "allOf", "$ref then allOf", "allOf with $ref"],
)
@pytest.mark.helper
def test_prepare(schema, schemas):
    """
    GIVEN schema, schemas and expected schema
    WHEN prepare is called with the schema and schemas
    THEN the expected schema is returned.
    """
    returned_schema = helpers.schema.prepare(schema=schema, schemas=schemas)

    assert returned_schema == {"key": "value"}


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"key": "value"}}),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"key": "value"}},
        ),
    ],
    ids=["$ref skip", "allOf skip"],
)
@pytest.mark.helper
def test_prepare_skip(schema, schemas):
    """
    GIVEN schema, schemas
    WHEN prepare is called with the schema and schemas and skip name
    THEN the an empty schema is returned.
    """
    returned_schema = helpers.schema.prepare(
        schema=schema, schemas=schemas, skip_name="RefSchema"
    )

    assert returned_schema == {}
