"""Tests for full relationship schema checking."""

# pylint: disable=too-many-lines

import pytest

from open_alchemy.schemas.validation.property_.relationship import full

TESTS = [
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"type": "object"}},
        (False, "foreign key target schema :: every model must define x-tablename"),
        id="x-to-one referenced schema no tablenamed",
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
                "properties": {"id": {"type": "integer"}},
            }
        },
        (True, None),
        id="x-to-one foreign key property default joined table inheritance",
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
            "backref property :: malformed schema :: The schema must be a dictionary. ",
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
            "backref property :: items :: the back reference schema must be an object",
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
        (False, "backref property :: items :: properties values must be dictionaries"),
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
                        "items": {
                            "allOf": [
                                {"type": "object", "properties": True},
                                {"type": "object", "properties": {}},
                            ]
                        },
                    },
                },
            }
        },
        (False, "backref property :: items :: properties values must be dictionaries"),
        id="many-to-one back reference multiple properties first not dictionary",
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
                            "allOf": [
                                {"type": "object", "properties": {}},
                                {"type": "object", "properties": True},
                            ]
                        },
                    },
                },
            }
        },
        (False, "backref property :: items :: properties values must be dictionaries"),
        id="many-to-one back reference multiple properties second not dictionary",
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
            "backref property :: items :: properties cannot contain the property name "
            "of the relartionship to avoid circular references",
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
            "backref property :: items :: property names must be contained in the "
            "model schema properties",
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
        (False, "backref property :: items :: property schema must be dictionaries"),
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
            "backref property :: items :: id :: type :: expected integer, actual is "
            "string.",
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
            "backref property :: items :: id :: format :: expected format 2, actual is "
            "format 1.",
        ),
        id="many-to-one back reference has property format different",
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
            "backref property :: items :: id :: maxLength :: expected 2, actual is 1.",
        ),
        id="many-to-one back reference has property maxLength different",
    ),
    # pytest.param(
    #     {"properties": {"id": {"type": "integer", "format": "format 1"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "integer", "format": "format 1"}
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (True, None),
    #     id="many-to-one back reference has property format",
    # ),
    # pytest.param(
    #     {"properties": {"name": {"type": "string"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "integer"},
    #                             "name": {"type": "string"},
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (False, None),
    #     id="many-to-one back reference has multiple property first not defined",
    # ),
    # pytest.param(
    #     {"properties": {"id": {"type": "integer"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "integer"},
    #                             "name": {"type": "string"},
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (False, None),
    #     id="many-to-one back reference has multiple property second not defined",
    # ),
    # pytest.param(
    #     {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "string"},
    #                             "name": {"type": "string"},
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (False, None),
    #     id="many-to-one back reference has multiple property first wrong type",
    # ),
    # pytest.param(
    #     {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "integer"},
    #                             "name": {"type": "integer"},
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (False, None),
    #     id="many-to-one back reference has multiple property second wrong type",
    # ),
    # pytest.param(
    #     {"properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
    #     "ref_schema",
    #     {"$ref": "#/components/schemas/RefSchema"},
    #     {
    #         "RefSchema": {
    #             "x-tablename": "ref_schema",
    #             "x-backref": "schemas",
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "integer"},
    #                 "schemas": {
    #                     "readOnly": True,
    #                     "type": "array",
    #                     "items": {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "integer"},
    #                             "name": {"type": "string"},
    #                         },
    #                     },
    #                 },
    #             },
    #         }
    #     },
    #     (True, None),
    #     id="many-to-one back reference has multiple property",
    # ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "allOf": [
                    {
                        "x-tablename": "ref_schema",
                        "x-inherits": True,
                        "type": "object",
                        "properties": {},
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
        (
            False,
            "foreign key target schema :: models must have at least 1 property "
            "themself",
        ),
        id="x-to-one foreign key property default single table inheritance",
    ),
    pytest.param(
        {},
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "allOf": [
                    {
                        "x-inherits": True,
                        "type": "object",
                        "properties": {"other": {}},
                    },
                    {"$ref": "#/components/schemas/ParentSchema"},
                ]
            },
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
        (True, None),
        id="x-to-one foreign key property default single table valid",
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
        (False, "ref_schema_id :: type :: expected integer, actual is string.",),
        id="x-to-one foreign key defined different type",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": True, "x-tablename": "schema", "properties": {}},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {"ref_schema_id": {"type": "string"}},
            },
        },
        (True, None,),
        id="x-to-one foreign key defined different type joined table inheritance",
    ),
    pytest.param(
        {
            "allOf": [
                {"x-inherits": True, "properties": {}},
                {"$ref": "#/components/schemas/ParentSchema"},
            ]
        },
        "ref_schema",
        {"$ref": "#/components/schemas/RefSchema"},
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
            "ParentSchema": {
                "x-tablename": "parent_schema",
                "properties": {"ref_schema_id": {"type": "string"}},
            },
        },
        (False, "ref_schema_id :: type :: expected integer, actual is string.",),
        id="x-to-one foreign key defined different type single table inheritance",
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
            "ref_schema_id :: format :: expected not to be defined, actual "
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
        (False, "ref_schema_id :: format :: expected int32, actual is not defined.",),
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
        (False, "ref_schema_id :: format :: expected int32, actual is int64.",),
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
            "ref_schema_id :: maxLength :: expected not to be defined, actual is 1.",
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
        (False, "ref_schema_id :: maxLength :: expected 2, actual is not defined.",),
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
        (False, "ref_schema_id :: maxLength :: expected 2, actual is 1.",),
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
            "ref_schema_id :: default :: expected not to be defined, actual is 1.",
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
        (False, "ref_schema_id :: default :: expected 2, actual is not defined.",),
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
        (False, "ref_schema_id :: default :: expected 2, actual is 1.",),
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
