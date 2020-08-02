"""Tests for relationship validation."""

import pytest

from open_alchemy.schemas.validation import relationship


@pytest.mark.parametrize(
    "property_name, property_schema, source_schema, schemas, expected_result",
    [
        pytest.param(
            "schema",
            {},
            {},
            {},
            (False, "malformed schema: Every property requires a type. ",),
        ),
        pytest.param(
            "schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            {"RefSchema": {"x-tablename": "ref_schema", "type": "object"}},
            (False, "foreign key targeted schema must have properties",),
        ),
        pytest.param(
            "schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (True, None,),
        ),
    ],
)
@pytest.mark.schemas
def test_check(property_name, property_schema, source_schema, schemas, expected_result):
    """
    GIVEN property name, schema, source schema, schemas and expected result
    WHEN check is called with the schemas, source schema, property name and property
        schema
    THEN the expected result is returned.
    """
    returned_result = relationship.check(
        schemas, source_schema, property_name, property_schema
    )

    assert returned_result == expected_result
