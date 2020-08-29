"""Tests for relationship validation."""

import pytest

from open_alchemy.schemas.validation.property_ import relationship


@pytest.mark.parametrize(
    "property_name, property_schema, parent_schema, schemas, expected_result",
    [
        pytest.param(
            "schema",
            {},
            {},
            {},
            (
                False,
                "malformed schema :: Every property requires a type. ",
            ),
            id="malformed relationship",
        ),
        pytest.param(
            "schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {},
            {"RefSchema": {"x-tablename": "ref_schema", "type": "object"}},
            (
                False,
                "foreign key target schema :: properties :: models must have at least "
                "1 property themself",
            ),
            id="malformed foreign key target",
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
            (
                True,
                None,
            ),
            id="valid",
        ),
    ],
)
@pytest.mark.schemas
def test_check(property_name, property_schema, parent_schema, schemas, expected_result):
    """
    GIVEN property name, schema, source schema, schemas and expected result
    WHEN check is called with the schemas, source schema, property name and property
        schema
    THEN the expected result is returned.
    """
    returned_result = relationship.check(
        schemas, parent_schema, property_name, property_schema
    )

    assert returned_result == expected_result
