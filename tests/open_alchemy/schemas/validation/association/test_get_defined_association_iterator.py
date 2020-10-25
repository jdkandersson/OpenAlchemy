"""Tests for _get_defined_association_iterator function in association validation."""

import pytest

from open_alchemy.schemas import validation


class TestGetDefinedAssociationIterator:
    """Tests for _get_defined_association_iterator."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param({}, {}, [], id="empty"),
        pytest.param({"Schema1": {}}, {}, [], id="single not constructable"),
        pytest.param(
            {"Schema1": {"x-tablename": "table_1"}}, {}, [], id="single mapping empty"
        ),
        pytest.param(
            {"Schema1": {"x-tablename": "table_1"}},
            {"table_2": True},
            [],
            id="single mapping miss",
        ),
        pytest.param(
            {"Schema1": {"x-tablename": "table_1"}},
            {"table_1": True},
            [("Schema1", {"x-tablename": "table_1"}, "table_1")],
            id="single mapping hit",
        ),
        pytest.param(
            {
                "Schema1": {
                    "allOf": [
                        {"x-tablename": "table_1"},
                        {"$ref": "#/components/schemas/RefSchema"},
                    ]
                },
                "RefSchema": {"x-tablename": "other_table"},
            },
            {"table_1": True},
            [
                (
                    "Schema1",
                    {
                        "allOf": [
                            {"x-tablename": "table_1"},
                            {"$ref": "#/components/schemas/RefSchema"},
                        ]
                    },
                    "table_1",
                )
            ],
            id="single mapping hit local ref local first",
        ),
        pytest.param(
            {
                "Schema1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-tablename": "table_1"},
                    ]
                },
                "RefSchema": {"x-tablename": "other_table"},
            },
            {"table_1": True},
            [
                (
                    "Schema1",
                    {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-tablename": "table_1"},
                        ]
                    },
                    "table_1",
                )
            ],
            id="single mapping hit local ref ref first",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table_1"},
                "Schema2": {"x-tablename": "table_2"},
            },
            {},
            [],
            id="multiple miss",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table_1"},
                "Schema2": {"x-tablename": "table_2"},
            },
            {"table_1": True},
            [("Schema1", {"x-tablename": "table_1"}, "table_1")],
            id="multiple first hit",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table_1"},
                "Schema2": {"x-tablename": "table_2"},
            },
            {"table_2": True},
            [("Schema2", {"x-tablename": "table_2"}, "table_2")],
            id="multiple second hit",
        ),
        pytest.param(
            {
                "Schema1": {"x-tablename": "table_1"},
                "Schema2": {"x-tablename": "table_2"},
            },
            {"table_1": True, "table_2": True},
            [
                ("Schema1", {"x-tablename": "table_1"}, "table_1"),
                ("Schema2", {"x-tablename": "table_2"}, "table_2"),
            ],
            id="multiple all hit",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schemas, mapping, expected_items", TESTS)
    def test_(schemas, mapping, expected_items):
        """
        GIVEN schemas, mapping and expected items
        WHEN _get_defined_association_iterator is called with the schemas and mapping
        THEN the expected items are returned.
        """
        returned_items = validation.association._get_defined_association_iterator(
            schemas=schemas, tablename_mapping=mapping
        )

        assert list(returned_items) == expected_items
