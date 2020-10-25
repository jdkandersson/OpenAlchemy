"""Tests for the get_association_property_iterator association helper."""

import pytest

from open_alchemy.schemas.helpers import association

TESTS = [
    pytest.param(
        {},
        [],
        id="empty",
    ),
    pytest.param(
        {"Schema": {"properties": {"prop_1": {"type": "integer"}}}},
        [],
        id="single schema not constructable",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [],
        id="single schema single property not association",
    ),
    pytest.param(
        {
            "Schema": {
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                }
            },
            "RefSchema": {"x-secondary": "association"},
        },
        [],
        id="single schema single association not constructable",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
            "RefSchema": {"x-secondary": "association"},
        },
        [
            (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            )
        ],
        id="single schema single association",
    ),
    pytest.param(
        {
            "Schema": {
                "x-tablename": "schema",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                    "prop_2": {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                },
            },
            "RefSchema": {"x-secondary": "association"},
        },
        [
            (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
            (
                (
                    "Schema",
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                        },
                    },
                ),
                (
                    "prop_2",
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
        ],
        id="single schema multiple association",
    ),
    pytest.param(
        {
            "Schema": {
                "allOf": [
                    {
                        "x-tablename": "schema",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                        },
                    },
                    {
                        "properties": {
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            },
                        }
                    },
                ]
            },
            "RefSchema": {"x-secondary": "association"},
        },
        [
            (
                (
                    "Schema",
                    {
                        "allOf": [
                            {
                                "x-tablename": "schema",
                                "properties": {
                                    "prop_1": {
                                        "type": "array",
                                        "key_1": "value 1",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                },
                            },
                            {
                                "properties": {
                                    "prop_2": {
                                        "type": "array",
                                        "key_2": "value 2",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                }
                            },
                        ]
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
            (
                (
                    "Schema",
                    {
                        "allOf": [
                            {
                                "x-tablename": "schema",
                                "properties": {
                                    "prop_1": {
                                        "type": "array",
                                        "key_1": "value 1",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                },
                            },
                            {
                                "properties": {
                                    "prop_2": {
                                        "type": "array",
                                        "key_2": "value 2",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                }
                            },
                        ]
                    },
                ),
                (
                    "prop_2",
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
        ],
        id="single schema allOf multiple association",
    ),
    pytest.param(
        {
            "Schema": {
                "allOf": [
                    {
                        "x-inherits": True,
                        "properties": {
                            "child_prop": {
                                "type": "array",
                                "child_key": "child value",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            "RefSchema": {"x-secondary": "association"},
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop": {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
        },
        [
            (
                (
                    "Schema",
                    {
                        "allOf": [
                            {
                                "x-inherits": True,
                                "properties": {
                                    "child_prop": {
                                        "type": "array",
                                        "child_key": "child value",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    }
                                },
                            },
                            {"$ref": "#/components/schemas/ParentSchema"},
                        ]
                    },
                ),
                (
                    "child_prop",
                    {
                        "type": "array",
                        "child_key": "child value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
            (
                (
                    "ParentSchema",
                    {
                        "x-tablename": "parent_schema",
                        "properties": {
                            "parent_prop": {
                                "type": "array",
                                "parent_key": "parent value",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "parent_prop",
                    {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
        ],
        id="single schema multiple association single table inheritance",
    ),
    pytest.param(
        {
            "Schema": {
                "allOf": [
                    {
                        "x-tablename": "child_table",
                        "x-inherits": True,
                        "properties": {
                            "child_prop": {
                                "type": "array",
                                "child_key": "child value",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            "RefSchema": {"x-secondary": "association"},
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "parent_prop": {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
        },
        [
            (
                (
                    "Schema",
                    {
                        "allOf": [
                            {
                                "x-inherits": True,
                                "x-tablename": "child_table",
                                "properties": {
                                    "child_prop": {
                                        "type": "array",
                                        "child_key": "child value",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    }
                                },
                            },
                            {"$ref": "#/components/schemas/ParentSchema"},
                        ]
                    },
                ),
                (
                    "child_prop",
                    {
                        "type": "array",
                        "child_key": "child value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
            (
                (
                    "ParentSchema",
                    {
                        "x-tablename": "parent_schema",
                        "properties": {
                            "parent_prop": {
                                "type": "array",
                                "parent_key": "parent value",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "parent_prop",
                    {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
        ],
        id="single schema multiple association joined table inheritance",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    }
                },
            },
            "RefSchema": {"x-secondary": "association"},
        },
        [
            (
                (
                    "Schema1",
                    {
                        "x-tablename": "schema_1",
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "prop_1",
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
            (
                (
                    "Schema2",
                    {
                        "x-tablename": "schema_2",
                        "properties": {
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        },
                    },
                ),
                (
                    "prop_2",
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ),
        ],
        id="multiple schema single association",
    ),
]


@pytest.mark.parametrize("schemas, expected_items", TESTS)
@pytest.mark.schemas
@pytest.mark.helper
def test_(schemas, expected_items):
    """
    GIVEN schemas and expected items
    WHEN get_association_property_iterator is called with the schemas
    THEN the expected items are returned.
    """

    returned_items = list(
        association.get_association_property_iterator(schemas=schemas)
    )

    assert list(returned_items) == expected_items
