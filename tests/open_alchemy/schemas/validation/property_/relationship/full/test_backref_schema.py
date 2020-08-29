"""Tests for full relationship schema checking."""

import pytest

from open_alchemy.schemas.validation.property_.relationship import full

TESTS = [
    pytest.param(
        {"properties": {}},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            }
        },
        (True, None),
        id="x-to-one back reference property not defined",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {"id": {"type": "integer"}, "schemas": True},
            }
        },
        (
            False,
            "foreign key target schema :: properties :: schemas :: property values "
            "must be dictionaries",
        ),
        id="x-to-one back reference property defined not dictionary",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "x-backref": "schemas",
                "type": "object",
                "properties": {"id": {"type": "integer"}, "schemas": {}},
            }
        },
        (False, "backref property :: the property must be readOnly"),
        id="x-to-one back reference property defined not readOnly",
    ),
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
                    "schemas": {"readOnly": "True"},
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: A readOnly property must be of "
            "type boolean. ",
        ),
        id="x-to-one back reference property defined readOnly invalid",
    ),
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
                    "schemas": {"readOnly": True},
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: Every property requires a type. ",
        ),
        id="x-to-one back reference property defined no type",
    ),
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
                    "schemas": {"readOnly": True, "type": "not array"},
                },
            }
        },
        (False, "backref property :: unexpected type, expected array actual not array"),
        id="many-to-one back reference property defined not array type",
    ),
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
                    "schemas": {"readOnly": True, "type": "array"},
                },
            }
        },
        (False, "backref property :: items must be defined"),
        id="many-to-one back reference property defined no items",
    ),
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
                    "schemas": {"readOnly": True, "type": "array", "items": True},
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: The items property must be of "
            "type dict. ",
        ),
        id="many-to-one back reference property defined items not dictionary",
    ),
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
                    "schemas": {"readOnly": True, "type": "array", "items": {}},
                },
            }
        },
        (
            False,
            "backref property :: malformed schema :: Every property requires a type. ",
        ),
        id="many-to-one back reference property defined items no type",
    ),
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
                        "items": {"type": "not object"},
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: the back reference schema must "
            "be an object",
        ),
        id="many-to-one back reference property defined items not object type",
    ),
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
                        "items": {"type": "object"},
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference property defined items no properties",
    ),
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
                        "items": {"type": "object", "properties": True},
                    },
                },
            }
        },
        (
            False,
            "backref property :: items :: properties :: value of properties must be a "
            "dictionary",
        ),
        id="many-to-one back reference items properties not dictionary",
    ),
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
                        "items": {"type": "object", "properties": {}},
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference property defined items properties empty",
    ),
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
                    "schemas": {"$ref": "#/components/schemas/BackReferenceProp"},
                },
            },
            "BackReferenceProp": {
                "readOnly": True,
                "type": "array",
                "items": {"type": "object", "properties": {}},
            },
        },
        (True, None),
        id="many-to-one back reference property defined $ref items properties empty",
    ),
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
                        "items": {
                            "$ref": "#/components/schemas/BackReferencePropItems"
                        },
                    },
                },
            },
            "BackReferencePropItems": {"type": "object", "properties": {}},
        },
        (True, None),
        id="many-to-one back reference property defined items $ref properties empty",
    ),
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
                        "allOf": [
                            {
                                "readOnly": True,
                                "type": "array",
                                "items": {"type": "object", "properties": {}},
                            }
                        ]
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference property defined allOf items properties empty",
    ),
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
                        "items": {"allOf": [{"type": "object", "properties": {}}]},
                    },
                },
            }
        },
        (True, None),
        id="many-to-one back reference property defined items allOf properties empty",
    ),
    pytest.param(
        {},
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
                    "schema": {"readOnly": True, "type": "array"},
                },
            }
        },
        (False, "backref property :: unexpected type, expected object actual array"),
        id="one-to-one back reference wrong type",
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
                        "properties": {"id": {"type": "integer"}},
                    },
                },
            }
        },
        (True, None),
        id="one-to-one back reference",
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
                    "schema": {"readOnly": True, "type": "array"},
                },
            }
        },
        (False, "backref property :: unexpected type, expected object actual array"),
        id="one-to-many back reference wrong type",
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
                        "properties": {"id": {"type": "integer"}},
                    },
                },
            }
        },
        (True, None),
        id="one-to-many back reference",
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
                    "schemas": {"readOnly": True, "type": "object"},
                },
            }
        },
        (False, "backref property :: unexpected type, expected array actual object"),
        id="many-to-many back reference wrong type",
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
                            "properties": {"id": {"type": "integer"}},
                        },
                    },
                },
            }
        },
        (True, None),
        id="many-to-many back reference",
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
