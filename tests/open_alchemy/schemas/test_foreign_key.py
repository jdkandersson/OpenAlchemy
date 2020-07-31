"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy.schemas import foreign_key


class TestDefinesBackref:
    """Tests for _defines_backref"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_result",
        [
            pytest.param({}, {}, False, id="empty"),
            pytest.param(
                {"type": "not relationship"},
                {},
                False,
                id="property not object nor array type",
            ),
            pytest.param({"type": "array"}, {}, False, id="array no items"),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "not relationship"}},
                False,
                id="$ref property not object nor array type",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-json": True}},
                False,
                id="many-to-one JSON",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-json": False}},
                True,
                id="many-to-one x-json False",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object"}},
                True,
                id="many-to-one no x-json",
            ),
            pytest.param(
                {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
                {"RefSchema": {"type": "object"}},
                True,
                id="many-to-one allOf",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-uselist": False, "x-json": True}},
                False,
                id="one-to-one JSON",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-uselist": False}},
                True,
                id="one-to-one",
            ),
            pytest.param(
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"RefSchema": {"type": "object", "x-json": True}},
                False,
                id="one-to-many JSON",
            ),
            pytest.param(
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"RefSchema": {"type": "object"}},
                True,
                id="one-to-many",
            ),
            pytest.param(
                {
                    "allOf": [
                        {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/RefSchema"},
                        }
                    ]
                },
                {"RefSchema": {"type": "object"}},
                True,
                id="one-to-many allOf",
            ),
            pytest.param(
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"RefSchema": {"type": "object", "x-secondary": "schema_ref_schema"}},
                False,
                id="many-to-many",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_(schema, schemas, expected_result):
        """
        GIVEN schema, schemas and expected result
        WHEN _requires_foreign_key is called with the schema and schemas
        THEN the expected result is returned.
        """
        result = foreign_key._requires_foreign_key(schemas, schema)

        assert result == expected_result
