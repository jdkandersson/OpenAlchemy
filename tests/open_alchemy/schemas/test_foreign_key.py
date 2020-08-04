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


CALC_F_K_PROP_ART_TESTS = [
    pytest.param(
        "Schema",
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
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one",
    ),
    pytest.param(
        "Schema",
        {"required": []},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one not required",
    ),
    pytest.param(
        "Schema",
        {"required": ["ref_schema"]},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": False,
            },
        ),
        id="many-to-one required",
    ),
    pytest.param(
        "Schema",
        {
            "x-tablename": "schema",
            "required": ["ref_schema"],
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (
            "RefSchema",
            "schema_ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="one-to-many required",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "format": "int32"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "format": "int32",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one format",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "string", "maxLength": 1}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "string",
                "maxLength": 1,
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one maxLength",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "default": 1}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "default": 1,
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": False,
            },
        ),
        id="many-to-one default",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-primary-key",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-autoincrement": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-autoincrement",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-index": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-index",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-unique": True}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-unique",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-foreign-key": "other.key"}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-foreign-key",
    ),
    pytest.param(
        "Schema",
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "x-kwargs": {}}},
            }
        },
        (
            "Schema",
            "ref_schema_id",
            {
                "type": "integer",
                "x-foreign-key": "ref_schema.id",
                "x-dict-ignore": True,
                "nullable": True,
            },
        ),
        id="many-to-one x-kwargs",
    ),
]


class TestCalculateForeignKeyPropertyArtifacts:
    """Tests for _calculate_foreign_key_property_artifacts"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "parent_name, parent_schema, property_name, property_schema, schemas, "
        "expected_schema",
        CALC_F_K_PROP_ART_TESTS,
    )
    @pytest.mark.schemas
    def test_(
        parent_name,
        parent_schema,
        property_name,
        property_schema,
        schemas,
        expected_schema,
    ):
        """
        GIVEN schemas, parent schema, property name and schema and expected schema
        WHEN _calculate_foreign_key_property_artifacts is called with the schemas,
            parent schema and property name and schema
        THEN the expected schema is returned.
        """
        returned_schema = foreign_key._calculate_foreign_key_property_artifacts(
            schemas, parent_name, parent_schema, property_name, property_schema
        )

        assert returned_schema == expected_schema


GET_SCHEMA_FOREIGN_KEYS_TESTS = [
    pytest.param(
        "Schema",
        {"properties": {"prop_1": {"type": "integer"}}},
        {},
        [],
        id="single property no foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/RefSchema1"},
                }
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-secondary": "schema_ref_schema",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [],
        id="single property many-to-many",
    ),
    pytest.param(
        "Schema",
        {"properties": {"ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}}},
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="single property foreign key",
    ),
    pytest.param(
        "OtherSchema",
        {"properties": {"ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"}}},
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            }
        },
        [
            (
                "OtherSchema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="single property foreign key different name",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {"RefSchema1": {"type": "integer"}, "RefSchema2": {"type": "integer"}},
        [],
        id="multiple property no foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {"type": "integer",},
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property first foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {"type": "integer",},
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property second foreign key",
    ),
    pytest.param(
        "Schema",
        {
            "properties": {
                "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
            }
        },
        {
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
            (
                "Schema",
                "ref_schema_2_prop_2",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_2.prop_2",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            ),
        ],
        id="multiple property all foreign keys",
    ),
    pytest.param(
        "Schema",
        {
            "allOf": [
                {"$ref": "#/components/schemas/ParentSchema"},
                {
                    "x-inherits": True,
                    "properties": {
                        "ref_schema_1": {"$ref": "#/components/schemas/RefSchema1"},
                    },
                },
            ]
        },
        {
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {
                    "ref_schema_2": {"$ref": "#/components/schemas/RefSchema2"},
                },
            },
            "RefSchema1": {
                "x-tablename": "ref_schema_1",
                "x-foreign-key-column": "prop_1",
                "type": "object",
                "properties": {"prop_1": {"type": "integer"}},
            },
            "RefSchema2": {
                "x-tablename": "ref_schema_2",
                "x-foreign-key-column": "prop_2",
                "type": "object",
                "properties": {"prop_2": {"type": "integer"}},
            },
        },
        [
            (
                "Schema",
                "ref_schema_1_prop_1",
                {
                    "type": "integer",
                    "x-foreign-key": "ref_schema_1.prop_1",
                    "x-dict-ignore": True,
                    "nullable": True,
                },
            )
        ],
        id="multiple property first foreign key inheritance",
    ),
]


class TestGetSchemaForeignKeys:
    """Tests for _get_schema_foreign_keys"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema_name, schema, schemas, expected_foreign_keys",
        GET_SCHEMA_FOREIGN_KEYS_TESTS,
    )
    @pytest.mark.schemas
    def test_(schema_name, schema, schemas, expected_foreign_keys):
        """
        GIVEN schema name and schema, schemas and expected backrefs
        WHEN _get_schema_foreign_keys is called with the schema name, schema and schemas
        THEN the expected backrefs are returned.
        """
        returned_backrefs = foreign_key._get_schema_foreign_keys(
            schemas, schema_name, schema
        )

        assert list(returned_backrefs) == expected_foreign_keys
