"""Tests for the calculate_property_schema association helper."""

import pytest

from open_alchemy.schemas.helpers import association

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
                "properties": {"column_1": {"type": "type 1", "x-primary-key": True}},
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


@pytest.mark.parametrize("schema, schemas, expected_name, expected_schema", TESTS)
@pytest.mark.schemas
@pytest.mark.helper
def test_(schema, schemas, expected_name, expected_schema):
    """
    GIVEN schema, schemas and expected name and schema
    WHEN calculate_property_schema is called with the schema and schemas
    THEN the expected name and schema is returned.
    """
    returned_name, returned_schema = association.calculate_property_schema(
        schema=schema, schemas=schemas
    )

    assert returned_name == expected_name
    assert returned_schema == expected_schema
