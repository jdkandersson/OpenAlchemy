"""Tests for backref schemas processing."""

import pytest

from open_alchemy.schemas import backref


class TestCalculateArtifacts:
    """Tests for _calculate_artifacts"""

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
        WHEN _calculate_artifacts is called with the schema and schemas
        THEN the expected schema is returned.
        """
        returned_schema = backref._calculate_artifacts("Schema", schemas, schema)

        assert returned_schema == expected_schema
