"""Tests for spec unique tablename."""

import pytest

from open_alchemy.schemas import validation

CHECK_TESTS = [
    pytest.param({}, True, None, id="empty"),
    pytest.param({"Schema1": {}}, True, None, id="single not constructable"),
    pytest.param({"Schema1": {"x-tablename": "table 1"}}, True, None, id="single"),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 2"},
        },
        True,
        None,
        id="multiple different",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"x-tablename": "table 1"},
                    {"$ref": "#/components/schemas/Schema2"},
                ]
            },
            "Schema2": {"x-tablename": "table 2"},
        },
        True,
        None,
        id="multiple different local first",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"$ref": "#/components/schemas/Schema2"},
                    {"x-tablename": "table 1"},
                ]
            },
            "Schema2": {"x-tablename": "table 2"},
        },
        True,
        None,
        id="multiple different local last",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 1"},
        },
        False,
        ("table 1", "already", "Schema1", "Schema2"),
        id="multiple same first order",
    ),
    pytest.param(
        {
            "Schema2": {"x-tablename": "table 1"},
            "Schema1": {"x-tablename": "table 1"},
        },
        False,
        ("table 1", "already", "Schema2", "Schema1"),
        id="multiple same second order",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 2"},
            "Schema3": {"x-tablename": "table 3"},
        },
        True,
        None,
        id="many different",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 1"},
            "Schema3": {"x-tablename": "table 3"},
        },
        False,
        ("table 1", "already", "Schema1", "Schema2"),
        id="many 2 same first 2",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 2"},
            "Schema3": {"x-tablename": "table 1"},
        },
        False,
        ("table 1", "already", "Schema1", "Schema3"),
        id="many 2 same first and last",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 2"},
            "Schema3": {"x-tablename": "table 2"},
        },
        False,
        ("table 2", "already", "Schema2", "Schema3"),
        id="many 2 same last",
    ),
    pytest.param(
        {
            "Schema1": {"x-tablename": "table 1"},
            "Schema2": {"x-tablename": "table 1"},
            "Schema3": {"x-tablename": "table 1"},
        },
        False,
        ("table 1", "already", "Schema1", "Schema2"),
        id="many all same",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-inherits": True, "x-tablename": "schema"},
                ]
            },
            "RefSchema": {"x-tablename": "ref_schema"},
        },
        True,
        None,
        id="inheritance joined table",
    ),
    pytest.param(
        {
            "Schema1": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-inherits": True},
                ]
            },
            "RefSchema": {"x-tablename": "ref_schema"},
        },
        True,
        None,
        id="inheritance single table",
    ),
]


@pytest.mark.schemas
@pytest.mark.validate
@pytest.mark.parametrize("schemas, expected_valid, expected_reasons", CHECK_TESTS)
def test_check(schemas, expected_valid, expected_reasons):
    """
    GIVEN schemas and expected result
    WHEN check is called with the schemas
    THEN the expected result is returned.
    """
    returned_result = validation.unique_tablename.check(schemas=schemas)

    assert returned_result.valid == expected_valid
    if expected_reasons is not None:
        for reason in expected_reasons:
            assert reason in returned_result.reason
    else:
        assert returned_result.reason is None
