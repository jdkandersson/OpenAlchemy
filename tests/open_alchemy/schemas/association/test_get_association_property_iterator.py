"""Tests for the association pre-processor."""

import copy

import pytest

from open_alchemy.schemas import association


class TestGetAssociationPropertyIterator:
    """Tests for _get_association_property_iterator."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {},
            [],
            id="empty",
        ),
        pytest.param(
            {"Schema": {"properties": {"prop_1": {"type": "integer"}}}},
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
            [
                (
                    {
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        }
                    },
                    {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                )
            ],
            id="single schema single association",
        ),
        pytest.param(
            {
                "Schema": {
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
                    }
                },
                "RefSchema": {"x-secondary": "association"},
            },
            [
                (
                    {
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
                        }
                    },
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
                (
                    {
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
                        }
                    },
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ],
            id="single schema multiple association",
        ),
        pytest.param(
            {
                "Schema": {
                    "allOf": [
                        {
                            "properties": {
                                "prop_1": {
                                    "type": "array",
                                    "key_1": "value 1",
                                    "items": {"$ref": "#/components/schemas/RefSchema"},
                                },
                            }
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
                    {
                        "allOf": [
                            {
                                "properties": {
                                    "prop_1": {
                                        "type": "array",
                                        "key_1": "value 1",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                }
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
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
                (
                    {
                        "allOf": [
                            {
                                "properties": {
                                    "prop_1": {
                                        "type": "array",
                                        "key_1": "value 1",
                                        "items": {
                                            "$ref": "#/components/schemas/RefSchema"
                                        },
                                    },
                                }
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
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
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
                    {
                        "type": "array",
                        "child_key": "child value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
                (
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
                    {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
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
                    {
                        "type": "array",
                        "child_key": "child value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
                (
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
                    {
                        "type": "array",
                        "parent_key": "parent value",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ],
            id="single schema multiple association joined table inheritance",
        ),
        pytest.param(
            {
                "Schema1": {
                    "properties": {
                        "prop_1": {
                            "type": "array",
                            "key_1": "value 1",
                            "items": {"$ref": "#/components/schemas/RefSchema"},
                        }
                    }
                },
                "Schema2": {
                    "properties": {
                        "prop_2": {
                            "type": "array",
                            "key_2": "value 2",
                            "items": {"$ref": "#/components/schemas/RefSchema"},
                        }
                    }
                },
                "RefSchema": {"x-secondary": "association"},
            },
            [
                (
                    {
                        "properties": {
                            "prop_1": {
                                "type": "array",
                                "key_1": "value 1",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        }
                    },
                    {
                        "type": "array",
                        "key_1": "value 1",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
                (
                    {
                        "properties": {
                            "prop_2": {
                                "type": "array",
                                "key_2": "value 2",
                                "items": {"$ref": "#/components/schemas/RefSchema"},
                            }
                        }
                    },
                    {
                        "type": "array",
                        "key_2": "value 2",
                        "items": {"$ref": "#/components/schemas/RefSchema"},
                    },
                ),
            ],
            id="multiple schema single association",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("schemas, expected_items", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(schemas, expected_items):
        """
        GIVEN schemas and expected items
        WHEN _get_association_property_iterator is called with the schemas
        THEN the expected items are returned.
        """
        original_schemas = copy.deepcopy(schemas)

        returned_items = list(
            association._get_association_property_iterator(schemas=schemas)
        )

        assert list(returned_items) == [
            (original_schemas, *items) for items in expected_items
        ]
