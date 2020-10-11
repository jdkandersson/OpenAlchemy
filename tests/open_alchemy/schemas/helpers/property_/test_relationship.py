"""Tests for relationship helpers."""

import pytest

from open_alchemy.schemas.helpers.property_ import relationship

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
@pytest.mark.schemas
@pytest.mark.helper
def test_get_ref_schema_many_to_x(property_schema, schemas):
    """
    GIVEN property schema and schemas
    WHEN get_ref_schema_many_to_x is called with the property schema and schemas
    THEN the referenced schema is returned.
    """
    returned_schema = relationship.get_ref_schema_many_to_x(
        property_schema=property_schema, schemas=schemas
    )

    assert returned_schema == {"key": "value"}
