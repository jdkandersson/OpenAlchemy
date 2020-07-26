"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref


class TestDefinesBackref:
    """Tests for _defines_backref"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_result",
        [
            pytest.param({}, {}, False, id="no items, allOf nor $ref"),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {}},
                False,
                id="$ref no backref",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="$ref backref",
            ),
            pytest.param({"allOf": []}, {}, False, id="allOf empty"),
            pytest.param(
                {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="allOf single $ref",
            ),
            pytest.param(
                {"allOf": [{"x-backref": "schema"}]},
                {},
                True,
                id="allOf single x-backref",
            ),
            pytest.param({"allOf": [{}]}, {}, False, id="allOf single no backref"),
            pytest.param(
                {"allOf": [{}, {}]}, {}, False, id="allOf multiple no backref"
            ),
            pytest.param(
                {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {}]},
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="allOf multiple first",
            ),
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema"},
                    ]
                },
                {"RefSchema": {}},
                True,
                id="allOf multiple second",
            ),
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema"},
                    ]
                },
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="allOf multiple all",
            ),
            pytest.param(
                {"items": {"$ref": "#/components/schemas/RefSchema"}},
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="items $ref backref",
            ),
            pytest.param(
                {"allOf": [{"items": {"$ref": "#/components/schemas/RefSchema"}}]},
                {"RefSchema": {"x-backref": "schema"}},
                True,
                id="items allOf $ref backref",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(schema, schemas, expected_result):
        """
        GIVEN schema, schemas and expected result
        WHEN _defines_backref is called with the schema and schemas
        THEN the expected result is returned.
        """
        returned_result = backref._defines_backref(schemas, schema)

        assert returned_result == expected_result


class TestCalculateSchema:
    """Tests for _calculate_schema"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_schema",
        [
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema"},
                    ]
                },
                {"RefSchema": {}},
                (
                    "RefSchema",
                    "schema",
                    {
                        "type": "array",
                        "items": {"type": "object", "x-de-$ref": "Schema"},
                    },
                ),
                id="many to one",
            ),
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema"},
                    ]
                },
                {"RefSchema": {"x-backref": "wrong_schema"}},
                (
                    "RefSchema",
                    "schema",
                    {
                        "type": "array",
                        "items": {"type": "object", "x-de-$ref": "Schema"},
                    },
                ),
                id="many to one backref local and remote",
            ),
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema", "x-uselist": True},
                    ]
                },
                {"RefSchema": {}},
                (
                    "RefSchema",
                    "schema",
                    {
                        "type": "array",
                        "items": {"type": "object", "x-de-$ref": "Schema"},
                    },
                ),
                id="many to one uselist True",
            ),
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema"},
                        {"x-backref": "schema", "x-uselist": False},
                    ]
                },
                {"RefSchema": {}},
                ("RefSchema", "schema", {"type": "object", "x-de-$ref": "Schema"}),
                id="one to one",
            ),
            pytest.param(
                {
                    "items": {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-backref": "schema"},
                        ]
                    }
                },
                {"RefSchema": {}},
                ("RefSchema", "schema", {"type": "object", "x-de-$ref": "Schema"}),
                id="one to many",
            ),
            pytest.param(
                {
                    "items": {
                        "allOf": [
                            {"$ref": "#/components/schemas/RefSchema"},
                            {"x-backref": "schema", "x-secondary": "schema_ref_schema"},
                        ]
                    }
                },
                {"RefSchema": {}},
                (
                    "RefSchema",
                    "schema",
                    {
                        "type": "array",
                        "items": {"type": "object", "x-de-$ref": "Schema"},
                    },
                ),
                id="many to many",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(schema, schemas, expected_schema):
        """
        GIVEN schema, schemas and expected schema
        WHEN _calculate_schema is called with the schema and schemas
        THEN the expected schema is returned.
        """
        returned_schema = backref._calculate_schema("Schema", schemas, schema)

        assert returned_schema == expected_schema


class TestGetSchemaBackrefs:
    """Tests for _get_schema_backrefs"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_backrefs",
        [
            pytest.param({}, {}, [], id="no properties"),
            pytest.param({"properties": {}}, {}, [], id="empty properties"),
            pytest.param(
                {"properties": {"prop_1": {}}}, {}, [], id="single property no backref"
            ),
            pytest.param(
                {
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    }
                },
                {"RefSchema1": {}},
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    )
                ],
                id="single property backref",
            ),
            pytest.param(
                {
                    "properties": {
                        "prop_1": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"},]
                        },
                        "prop_2": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema2"},]
                        },
                    }
                },
                {"RefSchema1": {}, "RefSchema2": {}},
                [],
                id="multiple property no backref",
            ),
            pytest.param(
                {
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        },
                        "prop_2": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema2"},]
                        },
                    }
                },
                {"RefSchema1": {}, "RefSchema2": {}},
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    )
                ],
                id="multiple property first backref",
            ),
            pytest.param(
                {
                    "properties": {
                        "prop_1": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"},]
                        },
                        "prop_2": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema2"},
                                {"x-backref": "schema2"},
                            ]
                        },
                    }
                },
                {"RefSchema1": {}, "RefSchema2": {}},
                [
                    (
                        "RefSchema2",
                        "schema2",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    )
                ],
                id="multiple property second backref",
            ),
            pytest.param(
                {
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        },
                        "prop_2": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema2"},
                                {"x-backref": "schema2"},
                            ]
                        },
                    }
                },
                {"RefSchema1": {}, "RefSchema2": {}},
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    ),
                    (
                        "RefSchema2",
                        "schema2",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    ),
                ],
                id="multiple property all backref",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(schema, schemas, expected_backrefs):
        """
        GIVEN schema, schemas and expected backrefs
        WHEN _get_schema_backrefs is called with the schema and schemas
        THEN the expected backrefs are returned.
        """
        returned_backrefs = backref._get_schema_backrefs(schemas, "Schema", schema)

        assert list(returned_backrefs) == expected_backrefs
