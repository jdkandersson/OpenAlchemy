"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy.schemas import foreign_key


class TestForeignKeyPropertyNotDefined:
    """Tests for _foreign_key_property_not_defined"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "parent_schema, property_name, property_schema, schemas, expected_result",
        [
            pytest.param(
                {},
                "ref_schema",
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    "RefSchema": {
                        "x-tablename": "ref_schema",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                },
                True,
                id="not defined",
            ),
            pytest.param(
                {
                    "properties": {
                        "ref_schema_id": {
                            "type": "integer",
                            "x-foreign-key": "ref_schema.id",
                        }
                    }
                },
                "ref_schema",
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    "RefSchema": {
                        "x-tablename": "ref_schema",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                },
                False,
                id="defined",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_valid(
        parent_schema, property_name, property_schema, schemas, expected_result
    ):
        """
        GIVEN schemas, parent schema, property name and schema and expected result
        WHEN _foreign_key_property_not_defined is called with the schemas, parent schema
            and property name and schema
        THEN the expected result is returned.
        """
        returned_result = foreign_key._foreign_key_property_not_defined(
            schemas, parent_schema, property_name, property_schema
        )

        assert returned_result == expected_result
