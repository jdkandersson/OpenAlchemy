"""Tests for the association pre-processor."""

import pytest

from open_alchemy.schemas import association

TESTS = [
    pytest.param({}, {}, id="empty"),
    pytest.param(
        {"Schema": {"properties": {"prop_1": {"type": "integer"}}}},
        {"Schema": {"properties": {"prop_1": {"type": "integer"}}}},
        id="single schema not association",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "x-secondary": "association",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
        },
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "x-secondary": "association",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
            "Association": {
                "type": "object",
                "x-tablename": "association",
                "properties": {
                    "parent_schema_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema.parent_prop_1",
                    },
                    "child_schema_child_prop_1": {
                        "type": "string",
                        "x-primary-key": True,
                        "x-foreign-key": "child_schema.child_prop_1",
                    },
                },
                "required": [
                    "parent_schema_parent_prop_1",
                    "child_schema_child_prop_1",
                ],
            },
        },
        id="single schema single association",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "x-secondary": "association",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
            "DefinedAssociation": {
                "type": "object",
                "x-tablename": "association",
                "properties": {
                    "parent_schema_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema.parent_prop_1",
                    },
                },
                "required": [
                    "parent_schema_parent_prop_1",
                ],
            },
        },
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "x-secondary": "association",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
            "DefinedAssociation": {
                "allOf": [
                    {
                        "type": "object",
                        "x-tablename": "association",
                        "properties": {
                            "child_schema_child_prop_1": {
                                "type": "string",
                                "x-primary-key": True,
                                "x-foreign-key": "child_schema.child_prop_1",
                            },
                        },
                    },
                    {
                        "type": "object",
                        "x-tablename": "association",
                        "properties": {
                            "parent_schema_parent_prop_1": {
                                "type": "integer",
                                "x-primary-key": True,
                                "x-foreign-key": "parent_schema.parent_prop_1",
                            },
                        },
                        "required": [
                            "parent_schema_parent_prop_1",
                        ],
                    },
                ]
            },
        },
        id="single schema single association defined",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                    "parent_prop_3": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    },
                },
            },
            "RefSchema1": {
                "x-tablename": "child_schema_1",
                "x-secondary": "association_1",
                "properties": {
                    "child_1_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
            "RefSchema2": {
                "x-tablename": "child_schema_2",
                "x-secondary": "association_2",
                "properties": {
                    "child_2_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
        },
        {
            "Schema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop_1": {"type": "integer", "x-primary-key": True},
                    "parent_prop_2": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                    "parent_prop_3": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema2"},
                    },
                },
            },
            "RefSchema1": {
                "x-tablename": "child_schema_1",
                "x-secondary": "association_1",
                "properties": {
                    "child_1_prop_1": {"type": "string", "x-primary-key": True}
                },
            },
            "RefSchema2": {
                "x-tablename": "child_schema_2",
                "x-secondary": "association_2",
                "properties": {
                    "child_2_prop_1": {"type": "string", "x-primary-key": True}
                },
            },
            "Association1": {
                "type": "object",
                "x-tablename": "association_1",
                "properties": {
                    "parent_schema_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema.parent_prop_1",
                    },
                    "child_schema_1_child_1_prop_1": {
                        "type": "string",
                        "x-primary-key": True,
                        "x-foreign-key": "child_schema_1.child_1_prop_1",
                    },
                },
                "required": [
                    "parent_schema_parent_prop_1",
                    "child_schema_1_child_1_prop_1",
                ],
            },
            "Association2": {
                "type": "object",
                "x-tablename": "association_2",
                "properties": {
                    "parent_schema_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema.parent_prop_1",
                    },
                    "child_schema_2_child_2_prop_1": {
                        "type": "string",
                        "x-primary-key": True,
                        "x-foreign-key": "child_schema_2.child_2_prop_1",
                    },
                },
                "required": [
                    "parent_schema_parent_prop_1",
                    "child_schema_2_child_2_prop_1",
                ],
            },
        },
        id="single schema multiple association",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "parent_schema_1",
                "properties": {
                    "schema_1_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                    },
                    "schema_1_parent_prop_2": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema"},
                                {"x-secondary": "association_schema_1"},
                            ]
                        },
                    },
                },
            },
            "Schema2": {
                "x-tablename": "parent_schema_2",
                "properties": {
                    "schema_2_parent_prop_1": {
                        "type": "number",
                        "x-primary-key": True,
                    },
                    "schema_2_parent_prop_2": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema"},
                                {"x-secondary": "association_schema_2"},
                            ]
                        },
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True},
                },
            },
        },
        {
            "Schema1": {
                "x-tablename": "parent_schema_1",
                "properties": {
                    "schema_1_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                    },
                    "schema_1_parent_prop_2": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema"},
                                {"x-secondary": "association_schema_1"},
                            ]
                        },
                    },
                },
            },
            "Schema2": {
                "x-tablename": "parent_schema_2",
                "properties": {
                    "schema_2_parent_prop_1": {
                        "type": "number",
                        "x-primary-key": True,
                    },
                    "schema_2_parent_prop_2": {
                        "type": "array",
                        "items": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema"},
                                {"x-secondary": "association_schema_2"},
                            ]
                        },
                    },
                },
            },
            "RefSchema": {
                "x-tablename": "child_schema",
                "properties": {
                    "child_prop_1": {"type": "string", "x-primary-key": True}
                },
            },
            "AssociationSchema1": {
                "type": "object",
                "x-tablename": "association_schema_1",
                "properties": {
                    "parent_schema_1_schema_1_parent_prop_1": {
                        "type": "integer",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema_1.schema_1_parent_prop_1",
                    },
                    "child_schema_child_prop_1": {
                        "type": "string",
                        "x-primary-key": True,
                        "x-foreign-key": "child_schema.child_prop_1",
                    },
                },
                "required": [
                    "parent_schema_1_schema_1_parent_prop_1",
                    "child_schema_child_prop_1",
                ],
            },
            "AssociationSchema2": {
                "type": "object",
                "x-tablename": "association_schema_2",
                "properties": {
                    "parent_schema_2_schema_2_parent_prop_1": {
                        "type": "number",
                        "x-primary-key": True,
                        "x-foreign-key": "parent_schema_2.schema_2_parent_prop_1",
                    },
                    "child_schema_child_prop_1": {
                        "type": "string",
                        "x-primary-key": True,
                        "x-foreign-key": "child_schema.child_prop_1",
                    },
                },
                "required": [
                    "parent_schema_2_schema_2_parent_prop_1",
                    "child_schema_child_prop_1",
                ],
            },
        },
        id="multiple schema single association",
    ),
]


@pytest.mark.parametrize("schemas, expected_schemas", TESTS)
@pytest.mark.schemas
@pytest.mark.association
def test_process(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN process is called with the schemas
    THEN the schemas are equal to the expected schemas.
    """
    association.process(schemas=schemas)

    assert schemas == expected_schemas
