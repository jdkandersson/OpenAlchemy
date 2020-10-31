"""Tests for _get_association_tablenames association schemas function."""

import pytest

from open_alchemy import types
from open_alchemy.schemas import association


class TestGetAssociationTablenames:
    """Tests for _get_association_tablenames."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param([], set(), id="empty"),
        pytest.param(
            [types.TNameSchema(name="Schema1", schema={"x-tablename": "table 1"})],
            {"table 1"},
            id="single",
        ),
        pytest.param(
            [
                types.TNameSchema(name="Schema1", schema={"x-tablename": "table 1"}),
                types.TNameSchema(name="Schema2", schema={"x-tablename": "table 2"}),
            ],
            {"table 1", "table 2"},
            id="multiple",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("association_schemas, expected_tablenames", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(association_schemas, expected_tablenames):
        """
        GIVEN association schemas and expected tablenames
        WHEN _get_association_tablenames is called with the association schemas
        THEN the expected tablenames are returned.
        """
        returned_tablenames = association._get_association_tablenames(
            association_schemas=association_schemas
        )

        assert returned_tablenames == expected_tablenames
