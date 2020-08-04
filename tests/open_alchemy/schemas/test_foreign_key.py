"""Tests for foreign key pre-processor."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import foreign_key


class TestRequiresForeignKey:
    """Tests for _requires_foreign_key"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas",
        [
            pytest.param({}, {}, id="invalid property",),
            pytest.param(
                {"$ref": "#/components/schemas/RefSchema"},
                {"RefSchema": {"type": "object", "x-tablename": True}},
                id="invalid relationship",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_invalid(schema, schemas):
        """
        GIVEN invalid schema, schemas
        WHEN _requires_foreign_key is called with the schema and schemas
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            foreign_key._requires_foreign_key(schemas, schema)

    @staticmethod
    @pytest.mark.parametrize(
        "schema, schemas, expected_result",
        [
            pytest.param({"type": "integer"}, {}, False, id="not relationship",),
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


class TestForeignKeyPropertyNotDefined:
    """Tests for _foreign_key_property_not_defined"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.schemas
    def test_invalid():
        """
        GIVEN schemas, invalid parent schema and property name and schema
        WHEN _foreign_key_property_not_defined is called with the schemas, parent schema
            and property name and schema
        THEN MalformedSchemaError is raised.
        """
        parent_schema = {}
        property_name = "ref_schema"
        property_schema = {"$ref": "#/components/schemas/RefSchema"}
        schemas = {"RefSchema": {"type": "object"}}

        with pytest.raises(exceptions.MalformedSchemaError):
            foreign_key._foreign_key_property_not_defined(
                schemas, parent_schema, property_name, property_schema
            )

    @staticmethod
    @pytest.mark.parametrize(
        "parent_schema, property_name, property_schema, schemas, expected_result",
        [
            pytest.param(
                {},
                "ref_schema",
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    "RefSchema": {
                        "x-tablename": "ref_schema",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                },
                True,
                id="not defined",
            ),
            pytest.param(
                {
                    "properties": {
                        "ref_schema_id": {
                            "type": "integer",
                            "x-foreign-key": "ref_schema.id",
                        }
                    }
                },
                "ref_schema",
                {"$ref": "#/components/schemas/RefSchema"},
                {
                    "RefSchema": {
                        "x-tablename": "ref_schema",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                },
                False,
                id="defined",
            ),
        ],
    )
    @pytest.mark.schemas
    def test_valid(
        parent_schema, property_name, property_schema, schemas, expected_result
    ):
        """
        GIVEN schemas, parent schema, property name and schema and expected result
        WHEN _foreign_key_property_not_defined is called with the schemas, parent schema
            and property name and schema
        THEN the expected result is returned.
        """
        returned_result = foreign_key._foreign_key_property_not_defined(
            schemas, parent_schema, property_name, property_schema
        )

        assert returned_result == expected_result
