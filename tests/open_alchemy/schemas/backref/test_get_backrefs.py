"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref


class TestGetBackrefs:
    """Tests for _get_backrefs"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schemas, expected_backrefs",
        [
            pytest.param({}, [], id="empty",),
            pytest.param({"Schema1": {}}, [], id="single schema not constructable",),
            pytest.param(
                {"Schema1": {"properties": {"prop_1": {}}}},
                [],
                id="single schema no backrefs",
            ),
            pytest.param(
                {
                    "Schema1": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_1": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema1"},
                                    {"x-backref": "schema1"},
                                ]
                            }
                        },
                    },
                    "RefSchema1": {},
                },
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema1"},
                        },
                    )
                ],
                id="single schema backref",
            ),
            pytest.param(
                {
                    "Schema1": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_1": {
                                "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
                            }
                        },
                    },
                    "RefSchema1": {},
                    "Schema2": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_2": {
                                "allOf": [{"$ref": "#/components/schemas/RefSchema2"}]
                            }
                        },
                    },
                    "RefSchema2": {},
                },
                [],
                id="multiple schemas no backref",
            ),
            pytest.param(
                {
                    "Schema1": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_1": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema1"},
                                    {"x-backref": "schema1"},
                                ]
                            }
                        },
                    },
                    "RefSchema1": {},
                    "Schema2": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_2": {
                                "allOf": [{"$ref": "#/components/schemas/RefSchema2"}]
                            }
                        },
                    },
                    "RefSchema2": {},
                },
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema1"},
                        },
                    ),
                ],
                id="multiple schemas first backref",
            ),
            pytest.param(
                {
                    "Schema1": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_1": {
                                "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
                            }
                        },
                    },
                    "RefSchema1": {},
                    "Schema2": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_2": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema2"},
                                    {"x-backref": "schema2"},
                                ]
                            }
                        },
                    },
                    "RefSchema2": {},
                },
                [
                    (
                        "RefSchema2",
                        "schema2",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema2"},
                        },
                    )
                ],
                id="multiple schemas second backref",
            ),
            pytest.param(
                {
                    "Schema1": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_1": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema1"},
                                    {"x-backref": "schema1"},
                                ]
                            }
                        },
                    },
                    "RefSchema1": {},
                    "Schema2": {
                        "x-tablename": "schema1",
                        "properties": {
                            "prop_2": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/RefSchema2"},
                                    {"x-backref": "schema2"},
                                ]
                            }
                        },
                    },
                    "RefSchema2": {},
                },
                [
                    (
                        "RefSchema1",
                        "schema1",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema1"},
                        },
                    ),
                    (
                        "RefSchema2",
                        "schema2",
                        {
                            "type": "array",
                            "items": {"type": "object", "x-de-$ref": "Schema2"},
                        },
                    ),
                ],
                id="multiple schemas all backref",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(schemas, expected_backrefs):
        """
        GIVEN schemas and expected backrefs
        WHEN _get_backrefs is called with the schemas
        THEN the expected backrefs are returned.
        """
        returned_backrefs = backref._get_backrefs(schemas=schemas)

        assert list(returned_backrefs) == expected_backrefs
