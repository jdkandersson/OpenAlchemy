"""Tests for merge allOf helper."""


import pytest

from open_alchemy import helpers


@pytest.mark.helper
def test_not_all_of():
    """
    GIVEN schema that does not have the allOf statement
    WHEN merge_all_of is called with the schema
    THEN the schema is returned.
    """
    schema = {"key": "value"}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_single():
    """
    GIVEN schema that has allOf statement with a single schema
    WHEN merge_all_of is called with the schema
    THEN the schema in allOf is returned.
    """
    schema = {"allOf": [{"key": "value"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_multiple():
    """
    GIVEN schema that has multiple schemas under allOf
    WHEN merge_all_of is called with the schema
    THEN the merged schema of all schemas under allOf is returned.
    """
    schema = {"allOf": [{"key_1": "value_1"}, {"key_2": "value_2"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key_1": "value_1", "key_2": "value_2"}


@pytest.mark.helper
def test_multiple_same_key():
    """
    GIVEN schema that has multiple schemas under allOf with the same key
    WHEN merge_all_of is called with the schema
    THEN the value of the last schema is assigned to the key in the returned schema.
    """
    schema = {"allOf": [{"key": "value_1"}, {"key": "value_2"}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value_2"}


@pytest.mark.helper
def test_nested_all_of():
    """
    GIVEN schema that has allOf statement with an allOf statement with a single schema
    WHEN merge_all_of is called with the schema
    THEN the schema in allOf is returned.
    """
    schema = {"allOf": [{"allOf": [{"key": "value"}]}]}

    return_schema = helpers.merge_all_of(schema=schema, schemas={})

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_ref():
    """
    GIVEN schema that has allOf statement with $ref to another schema
    WHEN merge_all_of is called with the schema
    THEN the $ref schema in allOf is returned.
    """
    schema = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"key": "value"}}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_ref_all_of():
    """
    GIVEN schema that has allOf statement with $ref to another schema with an allOf
        statement with a schema
    WHEN merge_all_of is called with the schema
    THEN the allOf $ref schema in allOf is returned.
    """
    schema = {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}
    schemas = {"RefSchema": {"allOf": [{"key": "value"}]}}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert return_schema == {"key": "value"}


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
    WHEN merge_all_of is called with the schema
    THEN the returned schema has the expected required property.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

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
    WHEN merge_all_of is called with the schema
    THEN the returned schema has the expected properties.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

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
    WHEN merge_all_of is called with the schema
    THEN the returned schema has the expected backrefs.
    """
    schema = {"allOf": all_of_schema}
    schemas = {}

    return_schema = helpers.merge_all_of(schema=schema, schemas=schemas)

    assert return_schema["x-backrefs"] == expected_backrefs
