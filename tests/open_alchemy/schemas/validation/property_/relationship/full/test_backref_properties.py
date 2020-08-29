"""Tests for full relationship schema checking."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import full

TESTS = [
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {"type": "object", "properties": {"ref_schema": {}}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: properties cannot contain the "
            "property name of the relartionship to avoid circular references",
        ),
        id="many-to-one back reference has property name",
    ),
    pytest.param(
        {"properties": {}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {"type": "object", "properties": {"id": {}}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: could not find id in the model "
            "schema",
        ),
        id="many-to-one back reference has property not in schema",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {"type": "object", "properties": {"id": True}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: property values must be "
            "dictionaries",
        ),
        id="many-to-one back reference has property not dictionary",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {"type": "object", "properties": {"id": {}}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: Every property requires a type. ",
        ),
        id="many-to-one back reference has property no type",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "string"}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: type :: expected "
            "integer, actual is string.",
        ),
        id="many-to-one back reference has property different type",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer"}},
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference has property",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "$ref": "#/components/schemas/BackReferenceProperty"
                                }
                            },
                        },
                    },
                },
            },
            "BackReferenceProperty": {"type": "integer"},
        },
        (True, None),
        id="many-to-one back reference has property $ref",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"allOf": [{"type": "integer"}]}},
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference has property allOf",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "format": True}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: A format value must be of type "
            "string. ",
        ),
        id="many-to-one back reference has property format not string",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "format": "format 2"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "format": "format 1"}
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: format :: expected "
            "format 2, actual is format 1.",
        ),
        id="many-to-one back reference has property format different",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "format": "format 1"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "format": "format 1"}
                            },
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference has property format",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "maxLength": True}
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: A maxLength value must be of type "
            "integer. ",
        ),
        id="many-to-one back reference has property maxLength not string",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "maxLength": 2}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "maxLength": 1}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: maxLength :: expected 2, "
            "actual is 1.",
        ),
        id="many-to-one back reference has property maxLength different",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "maxLength": 1}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "maxLength": 1}},
                        },
                    },
                },
            }
        },
        (
            True,
            None,
        ),
        id="many-to-one back reference has property maxLength",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "default": True}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: The default value does not "
            "conform to the schema. The value is: True ",
        ),
        id="many-to-one back reference has property default not string",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "default": 2}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "default": 1}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: default :: expected 2, "
            "actual is 1.",
        ),
        id="many-to-one back reference has property default different",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer", "default": 1}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "default": 1}},
                        },
                    },
                },
            }
        },
        (
            True,
            None,
        ),
        id="many-to-one back reference has property default",
    ),
    pytest.param(
        {"properties": {"name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: could not find id in the model "
            "schema",
        ),
        id="many-to-one back reference has multiple property first not defined",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: could not find name in the "
            "model schema",
        ),
        id="many-to-one back reference has multiple property second not defined",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "allOf": [
                                {
                                    "type": "object",
                                    "properties": {"id": {"type": "integer"}},
                                },
                                {
                                    "type": "object",
                                    "properties": {"name": {"type": "string"}},
                                },
                            ]
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: could not find name in the "
            "model schema",
        ),
        id="many-to-one back reference allOF multiple property second not defined",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: type :: expected "
            "integer, actual is "
            "string.",
        ),
        id="many-to-one back reference has multiple property first wrong type",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "integer"},
                            },
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: name :: type :: expected "
            "string, actual is integer.",
        ),
        id="many-to-one back reference has multiple property second wrong type",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "allOf": [
                                {
                                    "type": "object",
                                    "properties": {"id": {"type": "integer"}},
                                },
                                {
                                    "type": "object",
                                    "properties": {"name": {"type": "integer"}},
                                },
                            ]
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: name :: type :: expected "
            "string, actual is integer.",
        ),
        id="many-to-one back reference allOf multiple property second wrong type",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference has multiple property",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "allOf": [
                                {
                                    "type": "object",
                                    "properties": {"id": {"type": "integer"}},
                                },
                                {
                                    "type": "object",
                                    "properties": {"name": {"type": "string"}},
                                },
                            ]
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference allOf multiple property",
    ),
    pytest.param(
        {"properties": {"id": {"type": "integer"}}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schema",
                "x-uselist": False,
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schema": {
                        "readOnly": True,
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: properties :: id :: type :: expected integer, actual "
            "is string.",
        ),
        id="one-to-one back reference property wrong type",
    ),
    pytest.param(
        {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schema",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "schema": {
                        "readOnly": True,
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                    },
                },
            }
        },
        (
            False,
            "backref property :: properties :: id :: type :: expected integer, actual "
            "is string.",
        ),
        id="one-to-many back reference property wrong type",
    ),
    pytest.param(
        {
            "type": "object",
            "x-tablename": "schemas",
            "properties": {"id": {"type": "integer", "x-primary-key": True}},
        },
        "ref_schema",
        {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "x-secondary": "schema_ref_schema",
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "x-primary-key": True},
                    "schemas": {
                        "readOnly": True,
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"id": {"type": "string"}},
                        },
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: id :: type :: expected "
            "integer, actual is string.",
        ),
        id="many-to-many back reference property wrong type",
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
