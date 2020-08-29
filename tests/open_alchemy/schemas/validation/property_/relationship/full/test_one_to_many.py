"""Tests for full relationship schema checking."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import full

TESTS = [
    pytest.param(
        {},
        "ref_schemas",
        {"type": "array", "items": True},
        {"RefSchema": {}},
        (False, "malformed schema :: The items property must be of type dict. "),
        id="one-to-many property schema malformed",
    ),
    pytest.param(
        {},
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {}},
        (False, "foreign key target schema :: every model must define x-tablename"),
        id="one-to-many source schema no tablenamed",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"name": {"type": "string"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {}},
        (False, "foreign key targeted schema must have the id property"),
        id="one-to-many foreign key default not present",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-foreign-key-column": "name"}},
        (False, "foreign key targeted schema must have the name property"),
        id="one-to-many foreign key configured not present",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {"id": {}}},
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {}},
        (
            False,
            "id property :: malformed schema :: Every property requires a type. ",
        ),
        id="one-to-many foreign key default property invalid",
    ),
    pytest.param(
        {"x-tablename": "schema", "type": "object", "properties": {"name": {}}},
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-foreign-key-column": "name"}},
        (
            False,
            "name property :: malformed schema :: Every property requires a type. ",
        ),
        id="one-to-many foreign key configured property invalid",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (True, None),
        id="one-to-many foreign key property default valid",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"name": {"type": "string"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-foreign-key-column": "name", "x-tablename": "ref_schema"}},
        (True, None),
        id="one-to-many foreign key property configured valid",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "x-tablename": "schema",
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                }
            ]
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"x-tablename": "ref_schema"}},
        (True, None),
        id="one-to-many foreign key allOf property valid",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"properties": {"schema_ref_schemas_id": {}}}},
        (
            False,
            "schema_ref_schemas_id property :: malformed schema :: Every property "
            "requires a type. ",
        ),
        id="one-to-many foreign key defined property invalid",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {"RefSchema": {"properties": {"schema_ref_schemas_id": {"type": "string"}}}},
        (
            False,
            "schema_ref_schemas_id :: type :: expected integer, actual is string.",
        ),
        id="one-to-many foreign key defined different type",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (True, None),
        id="one-to-many foreign key defined same type",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "allOf": [
                    {
                        "x-tablename": "ref_schema",
                        "properties": {
                            "schema_ref_schemas_id": {
                                "type": "integer",
                                "x-foreign-key": "schema.id",
                            }
                        },
                    }
                ]
            }
        },
        (True, None),
        id="one-to-many allOf foreign key defined same type",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "format": "int32"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: format :: expected int32, actual is "
            "not defined.",
        ),
        id="one-to-many foreign key defined format only on source",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "format": "int64",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: format :: expected not to be defined, "
            "actual is int64.",
        ),
        id="one-to-many foreign key defined format only on referenced",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "format": "int32"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "format": "int64",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: format :: expected int32, actual is int64.",
        ),
        id="one-to-many foreign key defined different format",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "format": "int32"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "format": "int32",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (True, None),
        id="one-to-many foreign key defined same format",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "string", "maxLength": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "string",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: maxLength :: expected 1, actual is "
            "not defined.",
        ),
        id="one-to-many foreign key defined maxLength only on source",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "string"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "string",
                        "maxLength": 2,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: maxLength :: expected not to be "
            "defined, actual is 2.",
        ),
        id="one-to-many foreign key defined maxLength only on referenced",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "string", "maxLength": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "string",
                        "maxLength": 2,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: maxLength :: expected 1, actual is 2.",
        ),
        id="one-to-many foreign key defined different maxLength",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "string", "maxLength": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "string",
                        "maxLength": 1,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (True, None),
        id="one-to-many foreign key defined same maxLength",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "default": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: default :: expected 1, actual is not defined.",
        ),
        id="one-to-many foreign key defined default only on source",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "default": 2,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: default :: expected not to be defined, actual is "
            "2.",
        ),
        id="one-to-many foreign key defined default only on referenced",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "default": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "default": 2,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (
            False,
            "schema_ref_schemas_id :: default :: expected 1, actual is 2.",
        ),
        id="one-to-many foreign key defined different default",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer", "default": 1}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "default": 1,
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (True, None),
        id="one-to-many foreign key defined same default",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {"schema_ref_schemas_id": {"type": "integer"}},
            }
        },
        (False, "schema_ref_schemas_id must define a foreign key"),
        id="one-to-many foreign key defined no foreign key",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "x-foreign-key": "wrong key",
                    }
                },
            }
        },
        (
            False,
            "the x-foreign-key of schema_ref_schemas_id is wrong, expected schema.id, "
            "the actual is wrong key",
        ),
        id="one-to-many foreign key defined wrong foreign key",
    ),
    pytest.param(
        {
            "x-tablename": "schema",
            "type": "object",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schemas",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {
                    "schema_ref_schemas_id": {
                        "type": "integer",
                        "x-foreign-key": "schema.id",
                    }
                },
            }
        },
        (True, None),
        id="one-to-many foreign key defined right foreign key",
    ),
]


@pytest.mark.parametrize(
    "parent_schema, property_name, property_schema, schemas, expected_result",
    TESTS,
)
@pytest.mark.schemas
def test_check(parent_schema, property_name, property_schema, schemas, expected_result):
    """
    GIVEN schemas, the parent and property schema and the expected result
    WHEN check is called with the schemas and parent and property schema
    THEN the expected result is returned.
    """
    returned_result = full.check(schemas, parent_schema, property_name, property_schema)

    assert returned_result == expected_result
