"""Tests for the association pre-processor."""

import pytest

from open_alchemy.schemas import association


class TestCalculatePropertySchema:
    """Tests for _calculate_property_schema."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {"column_1": {"type": "type 1", "x-primary-key": True}},
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="single column",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {
                        "type": "type 1",
                        "x-primary-key": True,
                        "format": "format 1",
                    }
                },
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "format": "format 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="format single column",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {
                        "type": "type 1",
                        "x-primary-key": True,
                        "maxLength": 1,
                    }
                },
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "maxLength": 1,
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="maxLength single column",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/Schema1"},
            {
                "Schema1": {
                    "x-tablename": "table_1",
                    "properties": {
                        "column_1": {"type": "type 1", "x-primary-key": True}
                    },
                }
            },
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="$ref single column",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-tablename": "table_1",
                        "properties": {
                            "column_1": {"type": "type 1", "x-primary-key": True}
                        },
                    }
                ]
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="allOf single column",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {"column_1": {"$ref": "#/components/schemas/Column1"}},
            },
            {"Column1": {"type": "type 1", "x-primary-key": True}},
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="column $ref single column",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {"allOf": [{"type": "type 1", "x-primary-key": True}]}
                },
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="column allOf single column",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {"type": "type 1", "x-primary-key": True},
                    "column_2": {"type": "type 2"},
                    "column_3": {"type": "type 3"},
                },
            },
            {},
            "table_1_column_1",
            {
                "type": "type 1",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_1",
            },
            id="multiple column primary key first",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {"type": "type 1"},
                    "column_2": {"type": "type 2", "x-primary-key": True},
                    "column_3": {"type": "type 3"},
                },
            },
            {},
            "table_1_column_2",
            {
                "type": "type 2",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_2",
            },
            id="multiple column primary key middle",
        ),
        pytest.param(
            {
                "x-tablename": "table_1",
                "properties": {
                    "column_1": {"type": "type 1"},
                    "column_2": {"type": "type 2"},
                    "column_3": {"type": "type 3", "x-primary-key": True},
                },
            },
            {},
            "table_1_column_3",
            {
                "type": "type 3",
                "x-primary-key": True,
                "x-foreign-key": "table_1.column_3",
            },
            id="multiple column primary key end",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-inherits": True,
                        "properties": {
                            "child_column": {
                                "type": "child type",
                                "x-primary-key": True,
                            }
                        },
                    },
                    {"$ref": "#/components/schemas/Parent"},
                ],
            },
            {
                "Parent": {
                    "x-tablename": "parent_table",
                    "properties": {"parent_column": {"type": "parent type"}},
                }
            },
            "parent_table_child_column",
            {
                "type": "child type",
                "x-primary-key": True,
                "x-foreign-key": "parent_table.child_column",
            },
            id="single table inheritance primary key on child",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-inherits": True,
                        "properties": {"child_column": {"type": "child type"}},
                    },
                    {"$ref": "#/components/schemas/Parent"},
                ],
            },
            {
                "Parent": {
                    "x-tablename": "parent_table",
                    "properties": {
                        "parent_column": {"type": "parent type", "x-primary-key": True}
                    },
                }
            },
            "parent_table_parent_column",
            {
                "type": "parent type",
                "x-primary-key": True,
                "x-foreign-key": "parent_table.parent_column",
            },
            id="single table inheritance primary key on parent",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-tablename": "child_table",
                        "x-inherits": True,
                        "properties": {
                            "child_column": {
                                "type": "child type",
                                "x-primary-key": True,
                            }
                        },
                    },
                    {"$ref": "#/components/schemas/Parent"},
                ],
            },
            {
                "Parent": {
                    "x-tablename": "parent_table",
                    "properties": {
                        "parent_column": {"type": "parent type", "x-primary-key": True}
                    },
                }
            },
            "child_table_child_column",
            {
                "type": "child type",
                "x-primary-key": True,
                "x-foreign-key": "child_table.child_column",
            },
            id="joined table inheritance child first",
        ),
        pytest.param(
            {
                "allOf": [
                    {"$ref": "#/components/schemas/Parent"},
                    {
                        "x-tablename": "child_table",
                        "x-inherits": True,
                        "properties": {
                            "child_column": {
                                "type": "child type",
                                "x-primary-key": True,
                            }
                        },
                    },
                ],
            },
            {
                "Parent": {
                    "x-tablename": "parent_table",
                    "properties": {
                        "parent_column": {"type": "parent type", "x-primary-key": True}
                    },
                }
            },
            "child_table_child_column",
            {
                "type": "child type",
                "x-primary-key": True,
                "x-foreign-key": "child_table.child_column",
            },
            id="joined table inheritance parent first",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("schema, schemas, expected_name, expected_schema", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(schema, schemas, expected_name, expected_schema):
        """
        GIVEN schema, schemas and expected name and schema
        WHEN _calculate_property_schema is called with the schema and schemas
        THEN the expected name and schema is returned.
        """
        returned_name, returned_schema = association._calculate_property_schema(
            schema=schema, schemas=schemas
        )

        assert returned_name == expected_name
        assert returned_schema == expected_schema


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
            parent_schema=parent_schema,
            property_schema=property_schema,
            schemas=schemas,
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
            parent_schema=parent_schema,
            property_schema=property_schema,
            schemas=schemas,
        )

        assert returned_name == expected_name
