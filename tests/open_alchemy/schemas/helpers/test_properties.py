"""Tests for properties helpers."""

import pytest

from open_alchemy.schemas.validation.helpers import properties

CHECK_PROPS_VALUES_TEST = [
    pytest.param(
        {},
        {},
        None,
        id="empty",
    ),
    pytest.param(
        {"properties": True},
        {},
        (False, "value of properties must be a dictionary"),
        id="single invalid",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"properties": True}},
        (False, "value of properties must be a dictionary"),
        id="single $ref invalid",
    ),
    pytest.param(
        {"properties": {}},
        {},
        None,
        id="single valid",
    ),
    pytest.param(
        {"allOf": [{"properties": True}, {"properties": {}}]},
        {},
        (False, "value of properties must be a dictionary"),
        id="multiple first invalid",
    ),
    pytest.param(
        {"allOf": [{"properties": {}}, {"properties": True}]},
        {},
        (False, "value of properties must be a dictionary"),
        id="multiple second invalid",
    ),
    pytest.param(
        {"allOf": [{"properties": {}}, {"properties": {}}]},
        {},
        None,
        id="multiple valid",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", CHECK_PROPS_VALUES_TEST)
def test_check_properties_values(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check_properties_values is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = properties.check_properties_values(schema=schema, schemas=schemas)

    assert returned_result == expected_result


CHECK_PROPS_ITEMS_TEST = [
    pytest.param(
        {},
        {},
        None,
        id="empty",
    ),
    pytest.param(
        {"properties": {}},
        {},
        None,
        id="single empty",
    ),
    pytest.param(
        {"properties": {True: "value"}},
        {},
        (False, "property names must be strings, True is not"),
        id="single key not string",
    ),
    pytest.param(
        {"properties": {"key_1": "value"}},
        {},
        (False, "key_1 :: property values must be dictionaries"),
        id="single value not dict",
    ),
    pytest.param(
        {"properties": {"key_1": {}}},
        {},
        None,
        id="single",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"properties": {"key_1": {}}}},
        None,
        id="single $ref",
    ),
    pytest.param(
        {"properties": {True: {}, "key_2": {}}},
        {},
        (False, "property names must be strings, True is not"),
        id="multiple keys first invalid",
    ),
    pytest.param(
        {"properties": {"key_1": {}, True: {}}},
        {},
        (False, "property names must be strings, True is not"),
        id="multiple keys second invalid",
    ),
    pytest.param(
        {"properties": {"key_1": {}, "key_2": {}}},
        {},
        None,
        id="multiple keys",
    ),
    pytest.param(
        {"allOf": [{"properties": {True: {}}}, {"properties": {"key_2": {}}}]},
        {},
        (False, "property names must be strings, True is not"),
        id="multiple properties first invalid",
    ),
    pytest.param(
        {"allOf": [{"properties": {"key_1": {}}}, {"properties": {True: {}}}]},
        {},
        (False, "property names must be strings, True is not"),
        id="multiple properties second invalid",
    ),
    pytest.param(
        {"allOf": [{"properties": {"key_1": {}}}, {"properties": {"key_2": {}}}]},
        {},
        None,
        id="multiple properties",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", CHECK_PROPS_ITEMS_TEST)
@pytest.mark.schemas
def test_check_properties_items(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check_properties_items is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = properties.check_properties_items(schema=schema, schemas=schemas)

    assert returned_result == expected_result
