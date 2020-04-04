"""Tests for functions in OpenAlchemy __init__."""

from unittest import mock

import pytest

import open_alchemy
from open_alchemy import exceptions


class TestGetBase:
    """Tests for _get_base."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, exception",
        [
            ({"x-inherits": "Parent"}, {}, exceptions.InheritanceError),
            (
                {
                    "allOf": [
                        {"x-inherits": "Parent"},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                {"Parent": {"x-tablename": "parent"}},
                exceptions.InheritanceError,
            ),
        ],
        ids=["invalid parent", "parent not constructed"],
    )
    @pytest.mark.init
    def test_invalid(schema, schemas, exception):
        """
        GIVEN invalid schema and schemas and expected exception
        WHEN _get_base is called with the schema and schemas
        THEN the expected exception is raised.
        """
        with pytest.raises(exception):
            open_alchemy._get_base(schema=schema, schemas=schemas)

    @staticmethod
    @pytest.mark.parametrize(
        "schema",
        [{}, {"x-inherits": False}],
        ids=["x-inherits not present", "x-inherits false"],
    )
    @pytest.mark.init
    def test_not_inherit(schema):
        """
        GIVEN schema that does not inherit
        WHEN _get_base is called with the schema
        THEN the base is returned.
        """
        base = mock.MagicMock()
        setattr(open_alchemy.models, "Base", base)

        returned_base = open_alchemy._get_base(schema=schema, schemas={})

        assert returned_base == base

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas",
        [
            (
                {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                {"Parent": {"x-tablename": "parent"}},
            ),
            (
                {
                    "allOf": [
                        {"x-inherits": "Parent"},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                {"Parent": {"x-tablename": "parent"}},
            ),
        ],
        ids=["x-inherits true", "x-inherits string"],
    )
    @pytest.mark.init
    def test_inherit(schema, schemas):
        """
        GIVEN schema that inherits
        WHEN _get_base is called with the schema
        THEN the parent is returned.
        """
        parent = mock.MagicMock()
        setattr(open_alchemy.models, "Parent", parent)

        returned_base = open_alchemy._get_base(schema=schema, schemas=schemas)

        assert returned_base == parent
