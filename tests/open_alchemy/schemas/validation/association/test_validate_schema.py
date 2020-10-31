"""Tests for _validate_schema function in association validation."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import helpers
from open_alchemy.schemas import validation


class TestValidateSchema:
    """Tests for _validate_schema."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {"properties": {"prop_1": {}}},
            True,
            id="no primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True},
                    "prop_2": {"x-primary-key": True},
                    "prop_3": {"x-primary-key": True},
                }
            },
            False,
            id="too many primary key",
        ),
        pytest.param(
            {"properties": {"prop_1": {"x-primary-key": True}}},
            False,
            id="primary key no foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                    "prop_2": {"x-primary-key": True, "x-foreign-key": "foreign.key"},
                }
            },
            False,
            id="duplicate foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "wrong foreign key",
                    }
                }
            },
            False,
            id="primary key wrong foreign key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "x-primary-key": True,
                        "x-foreign-key": "ref_table.ref_column",
                        "type": "ref type",
                    }
                }
            },
            True,
            id="valid primary key",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, expected_valid", TESTS)
    def test_(schema, expected_valid):
        """
        GIVEN schema, schemas, and expected valid
        WHEN _validate_schema is called with the schema and schemas
        THEN the expected valid are returned.
        """
        name = "Schema"
        association = helpers.association.TParentPropertySchema(
            parent=types.TNameSchema(
                name="ParentSchema",
                schema={
                    "x-tablename": "parent_table",
                    "properties": {
                        "parent_column": {
                            "type": "parent type",
                            "x-primary-key": True,
                            "format": "parent format",
                            "maxLength": 1,
                        }
                    },
                },
            ),
            property=types.TNameSchema(
                name="PropertySchema",
                schema={"items": {"$ref": "#/components/schemas/RefSchema"}},
            ),
        )
        schemas = {
            "RefSchema": {
                "x-tablename": "ref_table",
                "x-secondary": "association",
                "properties": {
                    "ref_column": {"type": "ref type", "x-primary-key": True}
                },
            }
        }

        returned_result = validation.association._validate_schema(
            name=name, schema=schema, association=association, schemas=schemas
        )

        assert returned_result.valid == expected_valid
