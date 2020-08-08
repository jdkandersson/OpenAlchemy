"""Tests for validation rules."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import validation

PROCESS_TESTS = [
    pytest.param(True, True, id="not dictionary"),
    pytest.param({}, False, id="empty"),
    pytest.param({True: {}}, True, id="key not string"),
    pytest.param({"Schema1": True}, True, id="value not dict"),
    pytest.param({"Schema1": {}}, False, id="model not constructable"),
    pytest.param(
        {True: {}, "Schema2": {}}, True, id="multiple model first key not string"
    ),
    pytest.param(
        {"Schema1": {}, True: {}}, True, id="multiple model second key not string"
    ),
    pytest.param(
        {"Schema1": True, "Schema2": {}}, True, id="multiple model first value not dict"
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": True},
        True,
        id="multiple model second value not dict",
    ),
    pytest.param(
        {"Schema1": {}, "Schema2": {}}, False, id="multiple model not constructable"
    ),
    pytest.param({"Schema1": {"x-tablename": "schema_1"}}, True, id="model not valid"),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}},
            }
        },
        True,
        id="model property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        False,
        id="model valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}, "prop_2": {"type": "integer"}},
            }
        },
        True,
        id="model multiple properties first property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}, "prop_2": {}},
            }
        },
        True,
        id="model multiple properties second property not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {"type": "integer"},
                    "prop_2": {"type": "integer"},
                },
            }
        },
        False,
        id="model multiple properties valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        True,
        id="multiple model first not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {}},
            },
        },
        True,
        id="multiple model second not valid",
    ),
    pytest.param(
        {
            "Schema1": {
                "type": "object",
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "Schema2": {
                "type": "object",
                "x-tablename": "schema_2",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        False,
        id="multiple model valid",
    ),
]


@pytest.mark.parametrize("schemas, raises", PROCESS_TESTS)
@pytest.mark.schemas
def test_process(schemas, raises):
    """
    GIVEN schemas and whether an exception is expected
    WHEN process is called with the schemas
    THEN MalformedSchemaError is raised is raises is set otherwise it is not.
    """
    if raises:
        with pytest.raises(exceptions.MalformedSchemaError):
            validation.process(schemas=schemas)
    else:
        validation.process(schemas=schemas)
