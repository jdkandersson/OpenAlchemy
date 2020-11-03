"""Tests for relationship helpers."""

import pytest

from open_alchemy import types
from open_alchemy.helpers import relationship

CALCULATE_TYPE_TESTS = [
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.MANY_TO_ONE,
        id="many-to-one $ref",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.MANY_TO_ONE,
        id="many-to-one allOf",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-uselist": True}},
        types.RelationshipType.MANY_TO_ONE,
        id="many-to-one $ref uselist true",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object", "x-uselist": False}},
        types.RelationshipType.ONE_TO_ONE,
        id="one-to-one $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-uselist": False},
            ]
        },
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.ONE_TO_ONE,
        id="many-to-one allOf",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-uselist": False},
            ]
        },
        {"RefSchema": {"type": "object", "x-uselist": True}},
        types.RelationshipType.ONE_TO_ONE,
        id="many-to-one allOf and $ref",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.ONE_TO_MANY,
        id="many-to-one $ref",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/Schema"},
        {
            "Schema": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/RefSchema"},
            },
            "RefSchema": {"type": "object"},
        },
        types.RelationshipType.ONE_TO_MANY,
        id="$ref many-to-one $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                }
            ]
        },
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.ONE_TO_MANY,
        id="allOf many-to-one $ref",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema"},
                }
            ]
        },
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.ONE_TO_MANY,
        id="many-to-one allOf",
    ),
    pytest.param(
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"type": "object", "x-secondary": "schema_ref_schema"}},
        types.RelationshipType.MANY_TO_MANY,
        id="many-to-many $ref",
    ),
    pytest.param(
        {
            "type": "array",
            "items": {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "schema_ref_schema"},
                ]
            },
        },
        {"RefSchema": {"type": "object"}},
        types.RelationshipType.MANY_TO_MANY,
        id="many-to-many allOf",
    ),
]


@pytest.mark.parametrize(
    "schema, schemas, expected_type",
    CALCULATE_TYPE_TESTS,
)
@pytest.mark.helper
def test_calculate_type(schema, schemas, expected_type):
    """
    GIVEN schema, schemas and expected type
    WHEN calculate_type is called with the schema and schemas
    THEN the expected type is returned.
    """
    returned_type = relationship.calculate_type(schema=schema, schemas=schemas)

    assert returned_type == expected_type


GET_REF_SCHEMA_MANY_TO_X_TESTS = [
    pytest.param(
        {"items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"key": "value"}},
        id="simple",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/ItemsSchema"},
        {
            "ItemsSchema": {"items": {"$ref": "#/components/schemas/RefSchema"}},
            "RefSchema": {"key": "value"},
        },
        id="$ref",
    ),
    pytest.param(
        {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
        {"RefSchema": {"key": "value"}},
        id="allOf",
    ),
    pytest.param(
        {"items": {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]}},
        {"RefSchema": {"key": "value"}},
        id="items allOf",
    ),
]


@pytest.mark.parametrize("property_schema, schemas", GET_REF_SCHEMA_MANY_TO_X_TESTS)
@pytest.mark.helper
def test_get_ref_schema_many_to_x(property_schema, schemas):
    """
    GIVEN property schema and schemas
    WHEN get_ref_schema_many_to_x is called with the property schema and schemas
    THEN the referenced schema is returned.
    """
    returned_name, returned_schema = relationship.get_ref_schema_many_to_x(
        property_schema=property_schema, schemas=schemas
    )

    assert returned_name == "RefSchema"
    assert returned_schema == {"key": "value"}


IS_RELATIONSHIP_TYPE_TESTS = [
    pytest.param(
        {"type": "integer"},
        {},
        types.RelationshipType.MANY_TO_MANY,
        False,
        id="many-to-many simple",
    ),
    pytest.param(
        {"type": "object"},
        {},
        types.RelationshipType.MANY_TO_MANY,
        False,
        id="many-to-many relationship not many-to-many",
    ),
    pytest.param(
        {"type": "array", "items": {"x-secondary": "association"}},
        {},
        types.RelationshipType.MANY_TO_MANY,
        True,
        id="many-to-many relationship many-to-many",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "array", "items": {"x-secondary": "association"}}},
        types.RelationshipType.MANY_TO_MANY,
        True,
        id="many-to-many $ref relationship many-to-many",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "array", "items": {"x-secondary": "association"}}},
        types.RelationshipType.ONE_TO_MANY,
        False,
        id="one-to-many $ref relationship many-to-many",
    ),
    pytest.param(
        {"type": "array", "items": {}},
        {},
        types.RelationshipType.ONE_TO_MANY,
        True,
        id="one-to-many $ref relationship one-to-many",
    ),
]


@pytest.mark.parametrize(
    "property_schema, schemas, type_, expected_result", IS_RELATIONSHIP_TYPE_TESTS
)
@pytest.mark.helper
def test_is_relationship_type(property_schema, schemas, type_, expected_result):
    """
    GIVEN property schema, schemas, type and expected result
    WHEN is_relationship_type is called with the property schema, schemas and type
    THEN the expected result.
    """
    returned_result = relationship.is_relationship_type(
        type_=type_, schema=property_schema, schemas=schemas
    )

    assert returned_result == expected_result
