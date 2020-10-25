"""Tests for spec unique tablename."""

import pytest

from open_alchemy.schemas import validation

CHECK_TESTS = [
    pytest.param({"Schema1": {}}, True, None, id="single schema not constructable"),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        True,
        None,
        id="single schema single property not many-to-many",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    }
                },
            }
        },
        True,
        None,
        id="single schema single property many-to-many",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            }
        },
        True,
        None,
        id="single schema multiple property many-to-many different secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            }
        },
        False,
        ("Schema1", "prop_2", "association_1", "Schema1", "prop_1"),
        id="single schema multiple property many-to-many same secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_3"},
                    },
                },
            }
        },
        True,
        None,
        id="single schema many property many-to-many different secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_3"},
                    },
                },
            }
        },
        False,
        ("Schema1", "prop_2", "association_1", "Schema1", "prop_1"),
        id="single schema many property many-to-many same secondary first",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            }
        },
        False,
        ("Schema1", "prop_3", "association_1", "Schema1", "prop_1"),
        id="single schema many property many-to-many same secondary first and last",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            }
        },
        False,
        ("Schema1", "prop_3", "association_2", "Schema1", "prop_2"),
        id="single schema many property many-to-many same secondary last",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            }
        },
        False,
        ("Schema1", "prop_2", "association_1", "Schema1", "prop_2"),
        id="single schema many property many-to-many same secondary all",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            },
        },
        True,
        None,
        id="multiple schema single property many-to-many different secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
        },
        False,
        ("Schema2", "prop_2", "association_1", "Schema1", "prop_1"),
        id="multiple schema single property many-to-many same secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            },
            "Schema3": {
                "x-tablename": "schema_3",
                "properties": {
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_3"},
                    },
                },
            },
        },
        True,
        None,
        id="many schema single property many-to-many different secondary",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema3": {
                "x-tablename": "schema_3",
                "properties": {
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_3"},
                    },
                },
            },
        },
        False,
        ("Schema2", "prop_2", "association_1", "Schema1", "prop_1"),
        id="many schema single property many-to-many same secondary first",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            },
            "Schema3": {
                "x-tablename": "schema_3",
                "properties": {
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
        },
        False,
        ("Schema3", "prop_3", "association_1", "Schema1", "prop_1"),
        id="many schema single property many-to-many same secondary first last",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            },
            "Schema3": {
                "x-tablename": "schema_3",
                "properties": {
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_2"},
                    },
                },
            },
        },
        False,
        ("Schema3", "prop_3", "association_2", "Schema2", "prop_2"),
        id="many schema single property many-to-many same secondary last",
    ),
    pytest.param(
        {
            "Schema1": {
                "x-tablename": "schema_1",
                "properties": {
                    "prop_1": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema2": {
                "x-tablename": "schema_2",
                "properties": {
                    "prop_2": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
            "Schema3": {
                "x-tablename": "schema_3",
                "properties": {
                    "prop_3": {
                        "type": "array",
                        "items": {"x-secondary": "association_1"},
                    },
                },
            },
        },
        False,
        ("Schema2", "prop_2", "association_1", "Schema1", "prop_1"),
        id="many schema single property many-to-many same secondary all",
    ),
]


@pytest.mark.schemas
@pytest.mark.validate
@pytest.mark.parametrize("schemas, expected_valid, expected_reasons", CHECK_TESTS)
def test_check(schemas, expected_valid, expected_reasons):
    """
    GIVEN schemas and expected result
    WHEN check is called with the schemas
    THEN the expected result is returned.
    """
    returned_result = validation.unique_secondary.check(schemas=schemas)

    assert returned_result.valid == expected_valid
    if expected_reasons is not None:
        for reason in expected_reasons:
            assert reason in returned_result.reason
    else:
        assert returned_result.reason is None
