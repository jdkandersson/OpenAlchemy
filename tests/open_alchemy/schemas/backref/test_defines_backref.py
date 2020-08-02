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
