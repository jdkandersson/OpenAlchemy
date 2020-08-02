"""Tests for full relationship schema checking."""

import pytest

from open_alchemy.schemas.validation.relationship import full

TESTS = [
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        (False, "foreign key targeted schema must have a x-tablename value"),
        id="x-to-one referenced schema no tablenamed",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-tablename": True, "type": "object"}},
        (
            False,
            "malformed schema :: The x-tablename property must be of type string. ",
        ),
        id="x-to-one referenced schema tablenamed not string",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-tablename": "ref_schema", "type": "object"}},
        (False, "foreign key targeted schema must have properties"),
        id="x-to-one referenced schema no properties",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"name": {"type": "string"}},
            }
        },
        (False, "foreign key targeted schema must have the id property"),
        id="x-to-one foreign key default not present",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "x-foreign-key-column": "name",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (False, "foreign key targeted schema must have the name property"),
        id="x-to-one foreign key configured not present",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {}},
            }
        },
        (False, "id property :: malformed schema :: Every property requires a type. ",),
        id="x-to-one foreign key default property invalid",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "x-foreign-key-column": "name",
                "properties": {"name": {}},
            }
        },
        (
            False,
            "name property :: malformed schema :: Every property requires a type. ",
        ),
        id="x-to-one foreign key configured property invalid",
    ),
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
        (True, None),
        id="x-to-one foreign key property default valid",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "x-foreign-key-column": "name",
                "properties": {"name": {"type": "string"}},
            }
        },
        (True, None),
        id="x-to-one foreign key property configured valid",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "allOf": [
                    {
                        "x-tablename": "ref_schema",
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    }
                ]
            }
        },
        (True, None),
        id="x-to-one foreign key allOf property valid",
    ),
    pytest.param(
        {"properties": {"ref_schema_id": {}}},
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
            False,
            "ref_schema_id property :: malformed schema :: Every "
            "property requires a type. ",
        ),
        id="x-to-one foreign key defined invalid",
    ),
    pytest.param(
        {"properties": {"ref_schema_id": {"type": "string"}}},
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
            False,
            "the type of ref_schema_id is wrong, expected integer, actual is string.",
        ),
        id="x-to-one foreign key defined different type",
    ),
    pytest.param(
        {"properties": {"ref_schema_id": {}}},
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
            False,
            "ref_schema_id property :: malformed schema :: Every "
            "property requires a type. ",
        ),
        id="x-to-one foreign key defined property invalid",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "integer", "x-foreign-key": "ref_schema.id"}
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
        (True, None),
        id="x-to-one foreign key defined same type",
    ),
    pytest.param(
        {
            "allOf": [
                {
                    "properties": {
                        "ref_schema_id": {
                            "type": "integer",
                            "x-foreign-key": "ref_schema.id",
                        }
                    }
                }
            ]
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
        (True, None),
        id="x-to-one allOf foreign key defined same type",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "format": "int64",
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
        (
            False,
            "the format of ref_schema_id is wrong, expected not to be defined, actual "
            "is int64.",
        ),
        id="x-to-one foreign key defined format only on source",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "integer", "x-foreign-key": "ref_schema.id"}
            }
        },
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
            False,
            "the format of ref_schema_id is wrong, expected int32, actual is not "
            "defined.",
        ),
        id="x-to-one foreign key defined format only on referenced",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "format": "int64",
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
                "properties": {"id": {"type": "integer", "format": "int32"}},
            }
        },
        (
            False,
            "the format of ref_schema_id is wrong, expected int32, actual is int64.",
        ),
        id="x-to-one foreign key defined different format",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "format": "int32",
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
                "properties": {"id": {"type": "integer", "format": "int32"}},
            }
        },
        (True, None),
        id="x-to-one foreign key defined same format",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "string",
                    "maxLength": 1,
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
                "properties": {"id": {"type": "string"}},
            }
        },
        (
            False,
            "the maxLength of ref_schema_id is wrong, expected not to be defined, "
            "actual is 1.",
        ),
        id="x-to-one foreign key defined maxLength only on source",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "string", "x-foreign-key": "ref_schema.id"}
            }
        },
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "string", "maxLength": 2}},
            }
        },
        (
            False,
            "the maxLength of ref_schema_id is wrong, expected 2, actual is not "
            "defined.",
        ),
        id="x-to-one foreign key defined maxLength only on referenced",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "string",
                    "maxLength": 1,
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
                "properties": {"id": {"type": "string", "maxLength": 2}},
            }
        },
        (False, "the maxLength of ref_schema_id is wrong, expected 2, actual is 1.",),
        id="x-to-one foreign key defined different maxLength",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "string",
                    "maxLength": 2,
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
                "properties": {"id": {"type": "string", "maxLength": 2}},
            }
        },
        (True, None),
        id="x-to-one foreign key defined same maxLength",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "default": 1,
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
        (
            False,
            "the default of ref_schema_id is wrong, expected not to be defined, actual "
            "is 1.",
        ),
        id="x-to-one foreign key defined default only on source",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "integer", "x-foreign-key": "ref_schema.id"}
            }
        },
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer", "default": 2}},
            }
        },
        (
            False,
            "the default of ref_schema_id is wrong, expected 2, actual is not defined.",
        ),
        id="x-to-one foreign key defined default only on referenced",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "default": 1,
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
                "properties": {"id": {"type": "integer", "default": 2}},
            }
        },
        (False, "the default of ref_schema_id is wrong, expected 2, actual is 1.",),
        id="x-to-one foreign key defined different default",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {
                    "type": "integer",
                    "default": 2,
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
                "properties": {"id": {"type": "integer", "default": 2}},
            }
        },
        (True, None),
        id="x-to-one foreign key defined same default",
    ),
    pytest.param(
        {"properties": {"ref_schema_id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (False, "ref_schema_id must define a foreign key"),
        id="x-to-one foreign key defined no foreign key",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "integer", "x-foreign-key": "wrong key"}
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
        (
            False,
            "the x-foreign-key of ref_schema_id is wrong, expected ref_schema.id, the "
            "actual is wrong key",
        ),
        id="x-to-one foreign key defined wrong foreign key",
    ),
    pytest.param(
        {
            "properties": {
                "ref_schema_id": {"type": "integer", "x-foreign-key": "ref_schema.id"}
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
        (True, None),
        id="x-to-one foreign key defined right foreign key",
    ),
]


@pytest.mark.parametrize(
    "parent_schema, property_name, property_schema, schemas, expected_result", TESTS,
)
@pytest.mark.schemas
def test_check(parent_schema, property_name, property_schema, schemas, expected_result):
    """
    GIVEN schemas, the parent and property schema and the expected result
    WHEN check is called with the schemas and parent and property schema
    THEN the expected result is returned.
    """
    # pylint: disable=assignment-from-no-return
    returned_result = full.check(schemas, parent_schema, property_name, property_schema)

    assert returned_result == expected_result
