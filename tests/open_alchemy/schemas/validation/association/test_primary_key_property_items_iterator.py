"""Tests for _primary_key_property_items_iterator function in association validation."""

import pytest

from open_alchemy.schemas import validation


class TestPrimaryKeyPropertyItemsIterator:
    """Tests for _primary_key_property_items_iterator."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param({"properties": {}}, {}, [], id="empty properties"),
        pytest.param(
            {"properties": {"prop_1": {}}},
            {},
            [],
            id="single property not primary key",
        ),
        pytest.param(
            {"properties": {"prop_1": {"x-primary-key": False}}},
            {},
            [],
            id="single property primary key false",
        ),
        pytest.param(
            {"properties": {"prop_1": {"x-primary-key": True}}},
            {},
            [("prop_1", {"x-primary-key": True})],
            id="single property primary key",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"properties": {"prop_1": {"x-primary-key": True}}}},
            [("prop_1", {"x-primary-key": True})],
            id="$ref single property primary key",
        ),
        pytest.param(
            {"allOf": [{"properties": {"prop_1": {"x-primary-key": True}}}]},
            {},
            [("prop_1", {"x-primary-key": True})],
            id="allOf single property primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "allOf": [
                            {"x-primary-key": False},
                            {"$ref": "#/components/schemas/RefSchema"},
                        ]
                    }
                }
            },
            {"RefSchema": {"x-primary-key": True}},
            [],
            id="single property allOf not primary key $ref primary key local first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-primary-key": False},
                        ]
                    }
                }
            },
            {"RefSchema": {"x-primary-key": True}},
            [],
            id="single property allOf not primary key $ref primary key local first",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"key_1": "value 1"},
                    "prop_2": {"key_2": "value 2"},
                }
            },
            {},
            [],
            id="multiple property no primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "key_1": "value 1"},
                    "prop_2": {"key_2": "value 2"},
                }
            },
            {},
            [("prop_1", {"x-primary-key": True, "key_1": "value 1"})],
            id="multiple property first primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"key_1": "value 1"},
                    "prop_2": {"x-primary-key": True, "key_2": "value 2"},
                }
            },
            {},
            [("prop_2", {"x-primary-key": True, "key_2": "value 2"})],
            id="multiple property second primary key",
        ),
        pytest.param(
            {
                "properties": {
                    "prop_1": {"x-primary-key": True, "key_1": "value 1"},
                    "prop_2": {"x-primary-key": True, "key_2": "value 2"},
                }
            },
            {},
            [
                ("prop_1", {"x-primary-key": True, "key_1": "value 1"}),
                ("prop_2", {"x-primary-key": True, "key_2": "value 2"}),
            ],
            id="multiple property all primary key",
        ),
    ]

    @staticmethod
    @pytest.mark.schemas
    @pytest.mark.validate
    @pytest.mark.parametrize("schema, schemas, expected_items", TESTS)
    def test_(schema, schemas, expected_items):
        """
        GIVEN schema, schemas, and expected items
        WHEN _primary_key_property_items_iterator is called with the schema and schemas
        THEN the expected items are returned.
        """
        returned_items = validation.association._primary_key_property_items_iterator(
            schema=schema, schemas=schemas
        )

        assert list(returned_items) == expected_items
