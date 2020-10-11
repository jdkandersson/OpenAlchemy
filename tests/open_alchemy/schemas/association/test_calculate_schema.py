"""Tests for the association pre-processor."""

import pytest

from open_alchemy.schemas import association


class TestCalculateSchema:
    """Tests for _calculate_schema."""

    # pylint: disable=protected-access

    SCHEMA_TESTS = [
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {"items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "x-secondary": "association",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                }
            },
            id="items $ref",
        ),
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {
                "items": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-secondary": "association"},
                    ]
                }
            },
            {
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                }
            },
            id="items allOf",
        ),
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {"$ref": "#/components/schemas/ItemsSchema"},
            {
                "ItemsSchema": {"items": {"$ref": "#/components/schemas/RefSchema"}},
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "x-secondary": "association",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                },
            },
            id="$ref",
        ),
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
            {
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "x-secondary": "association",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                }
            },
            id="allOf",
        ),
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {
                "items": {
                    "allOf": [
                        {"x-secondary": "association"},
                        {"$ref": "#/components/schemas/RefSchema"},
                    ]
                }
            },
            {
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "x-secondary": "ref_association",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                }
            },
            id="items allOf secondary local and ref local first",
        ),
        pytest.param(
            {
                "x-tablename": "parent_table",
                "properties": {
                    "parent_column": {"type": "parent type", "x-primary-key": True}
                },
            },
            {
                "items": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-secondary": "association"},
                    ]
                }
            },
            {
                "RefSchema": {
                    "x-tablename": "ref_table",
                    "x-secondary": "ref_association",
                    "properties": {
                        "ref_column": {"type": "ref type", "x-primary-key": True}
                    },
                }
            },
            id="items allOf secondary local and ref ref first",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("parent_schema, property_schema, schemas", SCHEMA_TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_schema(parent_schema, property_schema, schemas):
        """
        GIVEN parent and property schema, schemas and expected schema
        WHEN _calculate_schema is called with the parent and property schema and schemas
        THEN the expected schema is returned.
        """
        _, returned_schema = association._calculate_schema(
            schemas,
            parent_schema,
            property_schema,
        )

        assert returned_schema == {
            "type": "object",
            "x-tablename": "association",
            "properties": {
                "parent_table_parent_column": {
                    "type": "parent type",
                    "x-primary-key": True,
                    "x-foreign-key": "parent_table.parent_column",
                },
                "ref_table_ref_column": {
                    "type": "ref type",
                    "x-primary-key": True,
                    "x-foreign-key": "ref_table.ref_column",
                },
            },
            "required": ["parent_table_parent_column", "ref_table_ref_column"],
        }

    NAME_TESTS = [
        pytest.param(
            "association",
            {},
            "Association",
            id="single word",
        ),
        pytest.param(
            "association_table",
            {},
            "AssociationTable",
            id="multiple word",
        ),
        pytest.param(
            "the_association_table",
            {},
            "TheAssociationTable",
            id="many words",
        ),
        pytest.param(
            "association",
            {"Other": {}},
            "Association",
            id="single unrelated additional key",
        ),
        pytest.param(
            "association",
            {"Association": {}},
            "AutogenAssociation",
            id="single additional key",
        ),
        pytest.param(
            "association",
            {"Association": {}, "AutogenAssociation": {}},
            "AutogenAutogenAssociation",
            id="multiple additional key",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("secondary, schemas_addition, expected_name", NAME_TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_name(secondary, schemas_addition, expected_name):
        """
        GIVEN parent and property schema, schemas and expected schema
        WHEN _calculate_schema is called with the parent and property schema and schemas
        THEN the expected name is returned.
        """
        parent_schema = {
            "x-tablename": "parent_table",
            "properties": {
                "parent_column": {"type": "parent type", "x-primary-key": True}
            },
        }
        property_schema = {"items": {"$ref": "#/components/schemas/RefSchema"}}
        schemas = {
            **schemas_addition,
            "RefSchema": {
                "x-tablename": "ref_table",
                "x-secondary": secondary,
                "properties": {
                    "ref_column": {"type": "ref type", "x-primary-key": True}
                },
            },
        }

        returned_name, _ = association._calculate_schema(
            schemas,
            parent_schema,
            property_schema,
        )

        assert returned_name == expected_name