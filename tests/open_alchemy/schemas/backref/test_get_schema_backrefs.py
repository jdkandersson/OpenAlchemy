"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref


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
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
                        },
                        "prop_2": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema2"}]
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
                            "allOf": [{"$ref": "#/components/schemas/RefSchema2"}]
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
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
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
            pytest.param(
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/ParentSchema"},
                        {
                            "x-inherits": True,
                            "properties": {
                                "prop_1": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/RefSchema1"},
                                        {"x-backref": "schema1"},
                                    ]
                                },
                            },
                        },
                    ]
                },
                {
                    "ParentSchema": {
                        "x-tablename": "parent_schema",
                        "properties": {
                            "prop_2": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema2"},
                                    {"x-backref": "schema2"},
                                ]
                            },
                        },
                    },
                    "RefSchema1": {},
                    "RefSchema2": {},
                },
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema"},
                        },
                    ),
                ],
                id="multiple property first backref inheritance",
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
