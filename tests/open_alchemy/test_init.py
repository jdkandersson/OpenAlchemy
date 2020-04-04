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
        "schemas, exception",
        [
            ({}, exceptions.SchemaNotFoundError),
            ({"Schema": {"x-inherits": "Parent"}}, exceptions.InheritanceError),
            (
                {
                    "Schema": {
                        "allOf": [
                            {"x-inherits": "Parent"},
                            {"$ref": "#/components/schemas/Parent"},
                        ]
                    },
                    "Parent": {"x-tablename": "parent"},
                },
                exceptions.InheritanceError,
            ),
        ],
        ids=["doesn't exist", "invalid parent", "parent not constructed"],
    )
    @pytest.mark.init
    def test_invalid(schemas, exception):
        """
        GIVEN invalid schemas and expected exception
        WHEN _get_base is called with the schema and schemas
        THEN the expected exception is raised.
        """
        name = "Schema"

        with pytest.raises(exception):
            open_alchemy._get_base(name=name, schemas=schemas)

    @staticmethod
    @pytest.mark.parametrize(
        "schemas",
        [{"Schema": {}}, {"Schema": {"x-inherits": False}}],
        ids=["x-inherits not present", "x-inherits false"],
    )
    @pytest.mark.init
    def test_not_inherit(schemas):
        """
        GIVEN schemas that does not inherit
        WHEN _get_base is called with the schema
        THEN the base is returned.
        """
        base = mock.MagicMock()
        setattr(open_alchemy.models, "Base", base)
        name = "Schema"

        returned_base = open_alchemy._get_base(name=name, schemas=schemas)

        assert returned_base == base

    @staticmethod
    @pytest.mark.parametrize(
        "schemas",
        [
            {
                "Schema": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                "Parent": {"x-tablename": "parent"},
            },
            {
                "Schema": {
                    "allOf": [
                        {"x-inherits": "Parent"},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                "Parent": {"x-tablename": "parent"},
            },
        ],
        ids=["x-inherits true", "x-inherits string"],
    )
    @pytest.mark.init
    def test_inherit(schemas):
        """
        GIVEN schema that inherits
        WHEN _get_base is called with the schema
        THEN the parent is returned.
        """
        name = "Schema"
        parent = mock.MagicMock()
        setattr(open_alchemy.models, "Parent", parent)

        returned_base = open_alchemy._get_base(name=name, schemas=schemas)

        assert returned_base == parent
