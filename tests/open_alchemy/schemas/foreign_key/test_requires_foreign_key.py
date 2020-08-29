"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy.schemas import foreign_key


class TestRequiresForeignKey:
    """Tests for _requires_foreign_key"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_result",
        [
            pytest.param(
                {"type": "integer"},
                {},
                False,
                id="not relationship",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
                True,
                id="many-to-one",
            ),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    "RefSchema": {
                        "type": "object",
                        "x-uselist": False,
                        "x-tablename": "ref_schema",
                        "x-backref": "schema",
                    }
                },
                True,
                id="one-to-one",
            ),
            pytest.param(
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {"RefSchema": {"type": "object", "x-tablename": "ref_schema"}},
                True,
                id="one-to-many",
            ),
            pytest.param(
                {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
                {
                    "RefSchema": {
                        "type": "object",
                        "x-secondary": "schema_ref_schema",
                        "x-tablename": "ref_schema",
                    }
                },
                False,
                id="many-to-many",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_valid(schema, schemas, expected_result):
        """
        GIVEN schema, schemas and expected result
        WHEN _requires_foreign_key is called with the schema and schemas
        THEN the expected result is returned.
        """
        result = foreign_key._requires_foreign_key(schemas, schema)

        assert result == expected_result
