"""Tests for merge allOf helper."""


import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_schema",
    [
        # THEN the schema is returned.
        ({"key": "value"}, {}, {"key": "value"}),
        # THEN the schema in allOf is returned.
        ({"allOf": [{"key": "value"}]}, {}, {"key": "value"}),
        # THEN the merged schema of all schemas under allOf is returned.
        (
            {"allOf": [{"key_1": "value_1"}, {"key_2": "value_2"}]},
            {},
            {"key_1": "value_1", "key_2": "value_2"},
        ),
        # THEN the value of the last schema is assigned to the key in the returned
        # schema.
        ({"allOf": [{"key": "value_1"}, {"key": "value_2"}]}, {}, {"key": "value_2"}),
        # THEN the schema in allOf is returned.
        ({"allOf": [{"allOf": [{"key": "value"}]}]}, {}, {"key": "value"}),
        # THEN the $ref schema in allOf is returned.
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"key": "value"}},
            {"key": "value"},
        ),
        # THEN the allOf $ref schema in allOf is returned.
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
            {"key": "value"},
        ),
    ],
    ids=[
        "allOf missing",
        "single",
        "multiple",
        "multiple same key",
        "nested allOf",
        "$ref",
        "$ref",
    ],
)
@pytest.mark.helper
def test_valid(schema, schemas, expected_schema):
    """
    GIVEN given schema, schemas and expected schema
    WHEN merge is called with the schema and schemas
    THEN the expected schema is returned.
    """
    return_schema = helpers.all_of.merge(schema=schema, schemas=schemas)

    assert return_schema == expected_schema


@pytest.mark.parametrize(
    "all_of_schema, expected_required",
    [
        ([{"required": ["id"]}, {}], ["id"]),
        ([{}, {"required": ["id"]}], ["id"]),
        ([{"required": ["id"]}, {"required": ["name"]}], ["id", "name"]),
        ([{"required": ["id"]}, {"required": ["id"]}], ["id"]),
    ],
    ids=["first only", "second only", "different", "common"],
)
@pytest.mark.helper
def test_required(all_of_schema, expected_required):
    """
    GIVEN schema that has allOf with schemas with given required properties and expected
        final required
    WHEN merge is called with the schema
    THEN the returned schema has the expected required property.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.all_of.merge(schema=schema, schemas=schemas)

    assert sorted(return_schema["required"]) == sorted(expected_required)


@pytest.mark.parametrize(
    "all_of_schema, expected_properties",
    [
        ([{"properties": {"key_1": "value 1"}}], {"key_1": "value 1"}),
        (
            [{"properties": {"key_1": "value 1", "key_2": "value 2"}}],
            {"key_1": "value 1", "key_2": "value 2"},
        ),
        ([{"properties": {"key_1": "value 1"}}, {}], {"key_1": "value 1"}),
        (
            [
                {"properties": {"key_1": "value 1"}},
                {"properties": {"key_2": "value 2"}},
            ],
            {"key_1": "value 1", "key_2": "value 2"},
        ),
        (
            [
                {"properties": {"key_1": "value 1"}},
                {"properties": {"key_1": "value 2"}},
            ],
            {"key_1": "value 2"},
        ),
    ],
    ids=[
        "single all of single property",
        "single all of multiple properties",
        "multiple all of one property",
        "multiple all of all properties",
        "multiple all of all properties duplicates",
    ],
)
@pytest.mark.helper
def test_properties(all_of_schema, expected_properties):
    """
    GIVEN schema that has allOf with schemas with given properties and expected
        properties
    WHEN merge is called with the schema
    THEN the returned schema has the expected properties.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.all_of.merge(schema=schema, schemas=schemas)

    assert return_schema["properties"] == expected_properties


@pytest.mark.parametrize(
    "all_of_schema, expected_backrefs",
    [
        ([{"x-backrefs": {"key_1": "value 1"}}], {"key_1": "value 1"}),
        (
            [{"x-backrefs": {"key_1": "value 1", "key_2": "value 2"}}],
            {"key_1": "value 1", "key_2": "value 2"},
        ),
        ([{"x-backrefs": {"key_1": "value 1"}}, {}], {"key_1": "value 1"}),
        (
            [
                {"x-backrefs": {"key_1": "value 1"}},
                {"x-backrefs": {"key_2": "value 2"}},
            ],
            {"key_1": "value 1", "key_2": "value 2"},
        ),
        (
            [
                {"x-backrefs": {"key_1": "value 1"}},
                {"x-backrefs": {"key_1": "value 2"}},
            ],
            {"key_1": "value 2"},
        ),
    ],
    ids=[
        "single all of single property",
        "single all of multiple backrefs",
        "multiple all of one property",
        "multiple all of all backrefs",
        "multiple all of all backrefs duplicates",
    ],
)
@pytest.mark.helper
def test_backrefs(all_of_schema, expected_backrefs):
    """
    GIVEN schema that has allOf with schemas with given backrefs and expected
        backrefs
    WHEN merge is called with the schema
    THEN the returned schema has the expected backrefs.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.all_of.merge(schema=schema, schemas=schemas)

    assert return_schema["x-backrefs"] == expected_backrefs
