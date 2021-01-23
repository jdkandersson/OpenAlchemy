"""Tests for schema helpers."""

import pytest

from open_alchemy.helpers import ref as ref_helper
from open_alchemy.helpers import schema as schema_helper


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        pytest.param(True, {}, False, id="not dict"),
        pytest.param({}, {}, False, id="empty"),
        pytest.param({"x-tablename": "table 1"}, {}, True, id="x-tablename"),
        pytest.param({"x-tablename": True}, {}, True, id="x-tablename not valid"),
        pytest.param({"x-inherits": "Schema1"}, {}, True, id="x-inherits string"),
        pytest.param({"x-inherits": True}, {}, True, id="x-inherits bool true"),
        pytest.param({"x-inherits": False}, {}, False, id="x-inherits bool false"),
        pytest.param({"x-inherits": 1}, {}, True, id="x-inherits not valid"),
        pytest.param({"$ref": True}, {}, False, id="$ref not string"),
        pytest.param(
            {"$ref": "#/components/schemas/Schema1"},
            {},
            False,
            id="$ref not resolve",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/Schema1"},
            {"Schema1": {"x-tablename": "table 1"}},
            False,
            id="x-tablename $ref only",
        ),
        pytest.param({"allOf": []}, {}, False, id="allOf empty"),
        pytest.param({"allOf": True}, {}, False, id="allOf not list"),
        pytest.param({"allOf": [True]}, {}, False, id="allOf elements not dict"),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/Schema1"}]},
            {"Schema1": {"x-tablename": "table 1"}},
            False,
            id="allOf x-tablename",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/Schema1"}, {"key": "value"}]},
            {"Schema1": {"x-tablename": "table 1"}},
            True,
            id="allOf x-tablename with additional",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "properties": {
                            "column": {"type": "integer", "x-primary-key": True}
                        },
                        "x-tablename": "table",
                        "type": "object",
                    }
                ]
            },
            {},
            True,
            id="allOf properties and tablename split",
        ),
    ],
)
@pytest.mark.helper
def test_constructable(schema, schemas, expected_result):
    """
    GIVEN schema and schemas
    WHEN constructable is called with the schema and schemas
    THEN the expected constructable is returned.
    """
    result = schema_helper.constructable(schema=schema, schemas=schemas)

    assert result == expected_result


@pytest.mark.helper
def test_constructable_remote(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN schema with remote $ref with x-tablename
    WHEN constructable is called with the schema
    THEN True is returned.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Table": {"x-tablename": "table 1"}}')
    # Set up remote schemas store
    ref_helper.set_context(path=str(schemas_file))
    schema = {"$ref": "remote.json#/Table"}

    result = schema_helper.constructable(schema=schema, schemas={})

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
    result = schema_helper.inherits(schema=schema, schemas={})

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
    returned_schema = schema_helper.prepare(schema=schema, schemas=schemas)

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
    returned_schema = schema_helper.prepare(
        schema=schema, schemas=schemas, skip_name="RefSchema"
    )

    assert returned_schema == {}


@pytest.mark.parametrize(
    "schema, schemas, expected_schema",
    [
        pytest.param({"key": "value"}, {}, {"key": "value"}, id="plain"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value"}},
            {"key": "value"},
            id="$ref",
        ),
        pytest.param({"allOf": [{"key": "value"}]}, {}, {"key": "value"}, id="allOf"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
            {"key": "value"},
            id="$ref then allOf",
        ),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
            {"key": "value"},
            id="allOf with $ref",
        ),
        pytest.param(
            {"properties": {}},
            {},
            {"properties": {}},
            id="object properties empty",
        ),
        pytest.param(
            {"properties": {"key_1": {"$ref": "#/components/schemas/RefSchema"}}},
            {"RefSchema": {"key": "value"}},
            {"properties": {"key_1": {"key": "value"}}},
            id="object property single $ref",
        ),
        pytest.param(
            {
                "properties": {
                    "key_1": {"$ref": "#/components/schemas/RefSchema1"},
                    "key_2": {"$ref": "#/components/schemas/RefSchema2"},
                }
            },
            {"RefSchema1": {"key_1": "value 1"}, "RefSchema2": {"key_2": "value 2"}},
            {
                "properties": {
                    "key_1": {"key_1": "value 1"},
                    "key_2": {"key_2": "value 2"},
                }
            },
            id="object property multiple $ref",
        ),
        pytest.param({"items": {}}, {}, {"items": {}}, id="array empty items"),
        pytest.param(
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"key": "value"}},
            {"items": {"key": "value"}},
            id="array empty items $ref",
        ),
    ],
)
@pytest.mark.helper
def test_prepare_deep(schema, schemas, expected_schema):
    """
    GIVEN schema, schemas and expected schema
    WHEN prepare_deep is called with the schema and schemas
    THEN the expected schema is returned.
    """
    returned_schema = schema_helper.prepare_deep(schema=schema, schemas=schemas)

    assert returned_schema == expected_schema
