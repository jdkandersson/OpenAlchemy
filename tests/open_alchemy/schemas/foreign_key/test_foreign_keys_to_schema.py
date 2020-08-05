"""Tests for foreign_key schemas processing."""

import pytest

from open_alchemy.schemas import foreign_key
from open_alchemy.schemas import helpers

Art = helpers.process.TArtifacts


class TestForeignKeysToSchema:
    """Tests for _foreign_keys_to_schema"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "foreign_keys, expected_schema",
        [
            pytest.param([], {"type": "object", "properties": {}}, id="empty"),
            pytest.param(
                [Art("Schema1", "prop_1", {"key_1": "value 1"})],
                {"type": "object", "properties": {"prop_1": {"key_1": "value 1"}}},
                id="single",
            ),
            pytest.param(
                [
                    Art("Schema1", "prop_1", {"key_1": "value 1"}),
                    Art("Schema1", "prop_2", {"key_2": "value 2"}),
                ],
                {
                    "type": "object",
                    "properties": {
                        "prop_1": {"key_1": "value 1"},
                        "prop_2": {"key_2": "value 2"},
                    },
                },
                id="multiple",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(foreign_keys, expected_schema):
        """
        GIVEN foreign keys and expected schema
        WHEN _foreign_keys_to_schema is called with the foreign keys
        THEN the expected schema is returned.
        """
        returned_schema = foreign_key._foreign_keys_to_schema(foreign_keys)

        assert returned_schema == expected_schema
