"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref
from open_alchemy.schemas import helpers

BackArt = helpers.process.Artifacts  # pylint: disable=protected-access


class TestGroupBackrefs:
    """Tests for _group_backrefs"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "backrefs, expected_backrefs",
        [
            pytest.param([], [], id="empty",),
            pytest.param(
                [BackArt("Schema1", "prop_1", {})],
                [("Schema1", [BackArt("Schema1", "prop_1", {})])],
                id="single",
            ),
            pytest.param(
                [BackArt("Schema1", "prop_1", {}), BackArt("Schema2", "prop_1", {})],
                [
                    ("Schema1", [BackArt("Schema1", "prop_1", {})]),
                    ("Schema2", [BackArt("Schema2", "prop_1", {})]),
                ],
                id="multiple different",
            ),
            pytest.param(
                [
                    BackArt("Schema1", "prop_1", {}),
                    BackArt("Schema1", "prop_2", {}),
                    BackArt("Schema2", "prop_1", {}),
                ],
                [
                    (
                        "Schema1",
                        [
                            BackArt("Schema1", "prop_1", {}),
                            BackArt("Schema1", "prop_2", {}),
                        ],
                    ),
                    ("Schema2", [BackArt("Schema2", "prop_1", {})]),
                ],
                id="multiple some different first multiple ordered",
            ),
            pytest.param(
                [
                    BackArt("Schema1", "prop_1", {}),
                    BackArt("Schema2", "prop_1", {}),
                    BackArt("Schema1", "prop_2", {}),
                ],
                [
                    (
                        "Schema1",
                        [
                            BackArt("Schema1", "prop_1", {}),
                            BackArt("Schema1", "prop_2", {}),
                        ],
                    ),
                    ("Schema2", [BackArt("Schema2", "prop_1", {})]),
                ],
                id="multiple some different first multiple not ordered",
            ),
            pytest.param(
                [
                    BackArt("Schema1", "prop_1", {}),
                    BackArt("Schema2", "prop_1", {}),
                    BackArt("Schema2", "prop_2", {}),
                ],
                [
                    ("Schema1", [BackArt("Schema1", "prop_1", {})]),
                    (
                        "Schema2",
                        [
                            BackArt("Schema2", "prop_1", {}),
                            BackArt("Schema2", "prop_2", {}),
                        ],
                    ),
                ],
                id="multiple some different second multiple",
            ),
            pytest.param(
                [BackArt("Schema1", "prop_1", {}), BackArt("Schema1", "prop_2", {})],
                [
                    (
                        "Schema1",
                        [
                            BackArt("Schema1", "prop_1", {}),
                            BackArt("Schema1", "prop_2", {}),
                        ],
                    )
                ],
                id="multiple same",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(backrefs, expected_backrefs):
        """
        GIVEN backrefs and expected backrefs
        WHEN _group_backrefs is called with the backrefs
        THEN the expected backrefs are returned.
        """
        returned_backrefs = backref._group_backrefs(backrefs=backrefs)
        returned_backrefs = [
            (name, list(backref_group)) for name, backref_group in returned_backrefs
        ]

        assert returned_backrefs == expected_backrefs
