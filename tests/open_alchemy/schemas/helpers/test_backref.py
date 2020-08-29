"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_backref",
    [
        pytest.param({}, {}, None, id="no items, allOf nor $ref"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            None,
            id="$ref no backref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="$ref backref",
        ),
        pytest.param({"allOf": []}, {}, None, id="allOf empty"),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="allOf single $ref",
        ),
        pytest.param(
            {"allOf": [{"x-backref": "schema"}]},
            {},
            "schema",
            id="allOf single x-backref",
        ),
        pytest.param({"allOf": [{}]}, {}, None, id="allOf single no backref"),
        pytest.param({"allOf": [{}, {}]}, {}, None, id="allOf multiple no backref"),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {}]},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="allOf multiple first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
            {"RefSchema": {}},
            "schema",
            id="allOf multiple second",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="allOf multiple all",
        ),
        pytest.param(
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="items $ref backref",
        ),
        pytest.param(
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="items allOf $ref backref",
        ),
    ],
)
@pytest.mark.schemas
def test_get(schema, schemas, expected_backref):
    """
    GIVEN schema, schemas and expected backref
    WHEN get is called with the schema and schemas
    THEN the expected backref is returned.
    """
    returned_backref = helpers.backref.get(schemas, schema)

    assert returned_backref == expected_backref


@pytest.mark.parametrize(
    "schema, schemas, expected_result",
    [
        pytest.param({}, {}, False, id="no items, allOf nor $ref"),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            False,
            id="$ref no backref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="$ref backref",
        ),
        pytest.param({"allOf": []}, {}, False, id="allOf empty"),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="allOf single $ref",
        ),
        pytest.param(
            {"allOf": [{"x-backref": "schema"}]},
            {},
            True,
            id="allOf single x-backref",
        ),
        pytest.param({"allOf": [{}]}, {}, False, id="allOf single no backref"),
        pytest.param({"allOf": [{}, {}]}, {}, False, id="allOf multiple no backref"),
        pytest.param(
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {}]},
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="allOf multiple first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
            {"RefSchema": {}},
            True,
            id="allOf multiple second",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "schema"},
                ]
            },
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="allOf multiple all",
        ),
        pytest.param(
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="items $ref backref",
        ),
        pytest.param(
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {"RefSchema": {"x-backref": "schema"}},
            True,
            id="items allOf $ref backref",
        ),
    ],
)
@pytest.mark.schemas
def test_defined(schema, schemas, expected_result):
    """
    GIVEN schema, schemas and expected result
    WHEN defined is called with the schema and schemas
    THEN the expected result is returned.
    """
    returned_result = helpers.backref.defined(schemas, schema)

    assert returned_result == expected_result
