"""Tests for properties helpers."""

import pytest

from open_alchemy.schemas.validation.helpers import properties

CHECK_PROPS_VALUES_TEST = [
    pytest.param({}, {}, None, id="empty",),
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
    pytest.param({"properties": {}}, {}, None, id="single valid",),
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
@pytest.mark.schemas
def test_check_properties_values(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN check_properties_values is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = properties.check_properties_values(schema=schema, schemas=schemas)

    assert returned_result == expected_result
