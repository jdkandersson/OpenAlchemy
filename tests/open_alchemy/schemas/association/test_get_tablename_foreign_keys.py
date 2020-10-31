"""Tests for _get_tablename_foreign_keys association schemas function."""

import pytest

from open_alchemy.schemas import association


class TestGetTablenameForeignKeys:
    """Tests for _get_tablename_foreign_keys."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param({}, {}, {}, id="empty"),
        pytest.param({}, {"Schema1": {}}, {}, id="single miss"),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {"Schema1": {}},
            {"table 1": ("Schema1", set())},
            id="single table single schema no properties",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {"Schema1": {"properties": {"prop_1": {}}}},
            {"table 1": ("Schema1", set())},
            id="single table single schema no foreign key",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {"Schema1": {"properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}}},
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id="single table single schema single foreign key",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {"$ref": "#/components/schemas/RefSchema"},
                "RefSchema": {
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}
                },
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id="single table single schema $ref single foreign key",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "allOf": [
                        {"properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}}
                    ]
                }
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id="single table single schema allOf single foreign key",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "properties": {"prop_1": {"$ref": "#/components/schemas/RefSchema"}}
                },
                "RefSchema": {"x-foreign-key": "foreign1.key1"},
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id="single table single schema single foreign key $ref",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "properties": {
                        "prop_1": {"allOf": [{"x-foreign-key": "foreign1.key1"}]}
                    }
                }
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id="single table single schema single foreign key allOf",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"x-foreign-key": "foreign1.key1"},
                                {"$ref": "#/components/schemas/RefSchema"},
                            ]
                        }
                    }
                },
                "RefSchema": {"x-foreign-key": "ref.key"},
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id=(
                "single table single schema single foreign key allOf local $ref "
                "local first"
            ),
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema"},
                                {"x-foreign-key": "foreign1.key1"},
                            ]
                        }
                    }
                },
                "RefSchema": {"x-foreign-key": "ref.key"},
            },
            {"table 1": ("Schema1", {"foreign1.key1"})},
            id=(
                "single table single schema single foreign key allOf local $ref "
                "$ref first"
            ),
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                )
            },
            {
                "Schema1": {
                    "properties": {
                        "prop_1": {"x-foreign-key": "foreign1.key1"},
                        "prop_2": {"x-foreign-key": "foreign1.key2"},
                    }
                }
            },
            {"table 1": ("Schema1", {"foreign1.key1", "foreign1.key2"})},
            id="single table single schema multiple foreign key",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1", "Schema2"]
                )
            },
            {
                "Schema1": {
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}
                },
                "Schema2": {
                    "properties": {"prop_2": {"x-foreign-key": "foreign2.key1"}}
                },
            },
            {"table 1": ("Schema1", {"foreign1.key1", "foreign2.key1"})},
            id="single table multiple schema single foreign key first parent",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema2", all_names=["Schema1", "Schema2"]
                )
            },
            {
                "Schema1": {
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}
                },
                "Schema2": {
                    "properties": {"prop_2": {"x-foreign-key": "foreign2.key1"}}
                },
            },
            {"table 1": ("Schema2", {"foreign1.key1", "foreign2.key1"})},
            id="single table multiple schema single foreign key second parent",
        ),
        pytest.param(
            {
                "table 1": association._TParentAllNames(
                    parent_name="Schema1", all_names=["Schema1"]
                ),
                "table 2": association._TParentAllNames(
                    parent_name="Schema2", all_names=["Schema2"]
                ),
            },
            {
                "Schema1": {
                    "properties": {"prop_1": {"x-foreign-key": "foreign1.key1"}}
                },
                "Schema2": {
                    "properties": {"prop_2": {"x-foreign-key": "foreign2.key1"}}
                },
            },
            {
                "table 1": ("Schema1", {"foreign1.key1"}),
                "table 2": ("Schema2", {"foreign2.key1"}),
            },
            id="multiple table single schema single foreign key",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize(
        "tablename_parent_all_names, schemas, expected_mapping", TESTS
    )
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(tablename_parent_all_names, schemas, expected_mapping):
        """
        GIVEN tablename names, schemas and expected mappng
        WHEN _get_tablename_foreign_keys is called with the schemas and tablenames
        THEN the expected mapping is returned.
        """
        returned_mapping = association._get_tablename_foreign_keys(
            tablename_parent_all_names=tablename_parent_all_names, schemas=schemas
        )

        assert returned_mapping == expected_mapping
