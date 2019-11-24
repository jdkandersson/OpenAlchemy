"""Tests for read_only handling."""

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory import read_only


class TestPrepareSchema:
    """Tests for _prepare_schema."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema",
        [
            {},
            {
                "readOnly": False,
                "type": "object",
                "properties": {"key": {"type": "simple_type"}},
            },
            {
                "readOnly": False,
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"key": {"type": "simple_type"}},
                },
            },
            {"readOnly": True},
            {"readOnly": True, "type": "simple_type"},
            {"readOnly": True, "type": "array"},
            {"readOnly": True, "type": "array", "items": {}},
            {"readOnly": True, "type": "array", "items": {"type": "simple_type"}},
            {"readOnly": True, "type": "array", "items": {"type": "array"}},
            {"readOnly": True, "type": "object"},
            {"readOnly": True, "type": "object", "properties": {}},
            {
                "readOnly": True,
                "type": "object",
                "properties": {"key": {"type": "array"}},
            },
            {
                "readOnly": True,
                "type": "object",
                "properties": {"key": {"type": "object"}},
            },
        ],
        ids=[
            "no readOnly",
            "readOnly False object",
            "readOnly False array",
            "no type",
            "not object nor array",
            "array no items",
            "array no items type",
            "array items type not object nor array",
            "array items type array",
            "object no properties",
            "object empty properties",
            "object property type array",
            "object property type object",
        ],
    )
    @pytest.mark.column
    def test_malformed(schema):
        """
        GIVEN malformed schema
        WHEN _prepare_schema is called
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            read_only._prepare_schema(schema=schema, schemas={})

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_schema",
        [
            (
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
                {},
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
            ),
            (
                {"$ref": "#/components/schemas/Schema"},
                {
                    "Schema": {
                        "type": "object",
                        "readOnly": True,
                        "properties": {"key": {"type": "simple_type"}},
                    }
                },
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
            ),
            (
                {
                    "allOf": [
                        {
                            "type": "object",
                            "readOnly": True,
                            "properties": {"key": {"type": "simple_type"}},
                        }
                    ]
                },
                {},
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
            ),
            (
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"$ref": "#/components/schemas/Property"}},
                },
                {"Property": {"type": "simple_type"}},
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
            ),
            (
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"allOf": [{"type": "simple_type"}]}},
                },
                {},
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {"key": {"type": "simple_type"}},
                },
            ),
            (
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {
                        "key_1": {"type": "simple_type_1"},
                        "key_2": {"type": "simple_type_2"},
                    },
                },
                {},
                {
                    "type": "object",
                    "readOnly": True,
                    "properties": {
                        "key_1": {"type": "simple_type_1"},
                        "key_2": {"type": "simple_type_2"},
                    },
                },
            ),
            (
                {
                    "type": "array",
                    "readOnly": True,
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "simple_type"}},
                    },
                },
                {},
                {
                    "type": "array",
                    "readOnly": True,
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "simple_type"}},
                    },
                },
            ),
            (
                {"$ref": "#/components/schemas/Schema"},
                {
                    "Schema": {
                        "type": "array",
                        "readOnly": True,
                        "items": {
                            "type": "object",
                            "properties": {"key": {"type": "simple_type"}},
                        },
                    }
                },
                {
                    "type": "array",
                    "readOnly": True,
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "simple_type"}},
                    },
                },
            ),
            (
                {
                    "allOf": [
                        {
                            "type": "array",
                            "readOnly": True,
                            "items": {
                                "type": "object",
                                "properties": {"key": {"type": "simple_type"}},
                            },
                        }
                    ]
                },
                {},
                {
                    "type": "array",
                    "readOnly": True,
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "simple_type"}},
                    },
                },
            ),
        ],
        ids=[
            "object",
            "object $ref",
            "object allOf",
            "object single property $ref",
            "object single property allOf",
            "object multiple properties",
            "array",
            "array $ref",
            "array allOf",
        ],
    )
    @pytest.mark.column
    def test_valid(schema, schemas, expected_schema):
        """
        GIVEN schema, schemas and expected schema
        WHEN _prepare_schema is called with the schema and schemas
        THEN the expected schema is returned.
        """
        returned_schema = read_only._prepare_schema(schema=schema, schemas=schemas)

        assert returned_schema == expected_schema
