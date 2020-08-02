"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref

BackArt = backref._BackrefArtifacts  # pylint: disable=protected-access


class TestGroupedBackrefsToSchemas:
    """Tests for _grouped_backrefs_to_schemas"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "grouped_backrefs, expected_schemas",
        [
            pytest.param([], [], id="empty"),
            pytest.param(
                [("Schema1", [BackArt("Schema1", "prop_1", {"key_1": "value 1"})])],
                [
                    (
                        "Schema1",
                        {
                            "type": "object",
                            "x-backrefs": {"prop_1": {"key_1": "value 1"}},
                        },
                    )
                ],
                id="single",
            ),
            pytest.param(
                [
                    ("Schema1", [BackArt("Schema1", "prop_1", {"key_1": "value 1"})]),
                    ("Schema2", [BackArt("Schema2", "prop_2", {"key_2": "value 2"})]),
                ],
                [
                    (
                        "Schema1",
                        {
                            "type": "object",
                            "x-backrefs": {"prop_1": {"key_1": "value 1"}},
                        },
                    ),
                    (
                        "Schema2",
                        {
                            "type": "object",
                            "x-backrefs": {"prop_2": {"key_2": "value 2"}},
                        },
                    ),
                ],
                id="multiple",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(grouped_backrefs, expected_schemas):
        """
        GIVEN grouped backrefs and expected schemas
        WHEN _grouped_backrefs_to_schemas is called with the grouped backrefs
        THEN the expected schemas are returned.
        """
        returned_schemas = backref._grouped_backrefs_to_schemas(
            grouped_backrefs=grouped_backrefs
        )

        assert list(returned_schemas) == expected_schemas
