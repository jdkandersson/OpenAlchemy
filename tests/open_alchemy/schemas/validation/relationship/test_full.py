"""Tests for full relationship schema checking."""

# pylint: disable=too-many-lines

import pytest

from open_alchemy.schemas.validation.relationship import full


@pytest.mark.parametrize(
    "source_schema, property_name, property_schema, schemas, expected_result",
    [
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            (False, "referenced schema must have a x-tablename value"),
            id="x-to-one referenced schema no tablenamed",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": True}},
            (False, "value of x-tablename must be a string"),
            id="x-to-one referenced schema tablenamed not string",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "ref_schema"}},
            (False, "referenced schema must have properties"),
            id="x-to-one referenced schema no properties",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "ref_schema", "properties": {}}},
            (False, "referenced schema must have the id property"),
            id="x-to-one foreign key default not present",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-foreign-key-column": "name",
                    "properties": {},
                }
            },
            (False, "referenced schema must have the name property"),
            id="x-to-one foreign key configured not present",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-tablename": "ref_schema", "properties": {"id": {}}}},
            (False, "referenced schema id property must define a type"),
            id="x-to-one foreign key default property invalid",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-foreign-key": "name",
                    "properties": {"name": {}},
                }
            },
            (False, "referenced schema name property must define a type"),
            id="x-to-one foreign key configured property invalid",
        ),
        pytest.param(
            {},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
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
                            "properties": {"id": {"type": "integer"}},
                        }
                    ]
                }
            },
            (True, None),
            id="x-to-one foreign key allOf property valid",
        ),
        pytest.param(
            {"properties": {"ref_schema_id": {"type": "string"}}},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (False, "the type of ref_schema_id must match the type of RefSchema.id"),
            id="x-to-one foreign key defined different type",
        ),
        pytest.param(
            {"properties": {"ref_schema_id": {}}},
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (False, "ref_schema_id must define a type"),
            id="x-to-one foreign key defined property invalid",
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
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (False, "ref_schema_id defines format but RefSchema.id does not"),
            id="x-to-one foreign key defined format only on source",
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
                    "properties": {"id": {"type": "integer", "format": "int32"}},
                }
            },
            (False, "ref_schema_id does not define format but RefSchema.id does"),
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
                    "properties": {"id": {"type": "integer", "format": "int32"}},
                }
            },
            (
                False,
                "the format of ref_schema_id must match the format of RefSchema.id",
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
                    "properties": {"id": {"type": "string"}},
                }
            },
            (False, "ref_schema_id defines maxLength but RefSchema.id does not"),
            id="x-to-one foreign key defined maxLength only on source",
        ),
        pytest.param(
            {
                "properties": {
                    "ref_schema_id": {
                        "type": "string",
                        "x-foreign-key": "ref_schema.id",
                    }
                }
            },
            "ref_schema",
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "properties": {"id": {"type": "string", "maxLength": 2}},
                }
            },
            (False, "ref_schema_id does not define maxLength but RefSchema.id does"),
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
                    "properties": {"id": {"type": "string", "maxLength": 2}},
                }
            },
            (
                False,
                "the maxLength of ref_schema_id must match the maxLength of "
                "RefSchema.id",
            ),
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
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (False, "ref_schema_id defines default but RefSchema.id does not"),
            id="x-to-one foreign key defined default only on source",
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
                    "properties": {"id": {"type": "integer", "default": 2}},
                }
            },
            (False, "ref_schema_id does not define default but RefSchema.id does"),
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
                    "properties": {"id": {"type": "integer", "default": 2}},
                }
            },
            (
                False,
                "the default of ref_schema_id must match the default of "
                "RefSchema.id",
            ),
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
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (False, "ref_schema_id must define a foreign key to RefSchema.id"),
            id="x-to-one foreign key defined wrong foreign key",
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
                    "properties": {"id": {"type": "integer"}},
                }
            },
            (True, None),
            id="x-to-one foreign key defined right foreign key",
        ),
        pytest.param(
            {},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "source schema must have a x-tablename value"),
            id="one-to-many source schema no tablenamed",
        ),
        pytest.param(
            {"x-tablename": True},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "value of x-tablename must be a string"),
            id="one-to-many source schema tablenamed not string",
        ),
        pytest.param(
            {"x-tablename": "schema"},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "source schema must have properties"),
            id="one-to-many source schema no properties",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {}},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "source schema must have the id property"),
            id="one-to-many foreign key default not present",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-foreign-key-column": "name"}},
            (False, "source schema must have the name property"),
            id="one-to-many foreign key configured not present",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {}}},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "source schema id property must define a type"),
            id="one-to-many foreign key default property invalid",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"name": {}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-foreign-key": "name"}},
            (False, "source schema name property must define a type"),
            id="one-to-many foreign key configured property invalid",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {}},
            (False, "referenced schema must have a x-tablename value"),
            id="one-to-many referenced no tablename",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-tablename": True}},
            (False, "value of x-tablename must be a string"),
            id="one-to-many referenced tablename not string",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"x-tablename": "ref_schema"}},
            (True, None),
            id="one-to-many foreign key property default valid",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"name": {"type": "string"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-foreign-key-column": "name",
                    "x-tablename": "ref_schema",
                }
            },
            (True, None),
            id="one-to-many foreign key property configured valid",
        ),
        pytest.param(
            {
                "allOf": [
                    {
                        "x-tablename": "schema",
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
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {"RefSchema": {"properties": {"schema_ref_schemas_id": {}}}},
            (False, "RefSchema.schema_ref_schemas_id must define a type"),
            id="one-to-many foreign key defined property invalid",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "properties": {"schema_ref_schemas_id": {"type": "string"}}
                }
            },
            (
                False,
                "the type of id must match the type of RefSchema.schema_ref_schemas_id",
            ),
            id="one-to-many foreign key defined different type",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
            (False, "id defines format but RefSchema.schema_ref_schemas_id does not"),
            id="one-to-many foreign key defined format only on source",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
                "id does not define format but RefSchema.schema_ref_schemas_id does",
            ),
            id="one-to-many foreign key defined format only on referenced",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
                "the format of id must match the format of "
                "RefSchema.schema_ref_schemas_id",
            ),
            id="one-to-many foreign key defined different format",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
                "id defines maxLength but RefSchema.schema_ref_schemas_id does not",
            ),
            id="one-to-many foreign key defined maxLength only on source",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "string"}},},
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
                "id does not define maxLength but RefSchema.schema_ref_schemas_id does",
            ),
            id="one-to-many foreign key defined maxLength only on referenced",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
                "the maxLength of id must match the maxLength of "
                "RefSchema.schema_ref_schemas_id",
            ),
            id="one-to-many foreign key defined different maxLength",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
            (False, "id defines default but RefSchema.schema_ref_schemas_id does not"),
            id="one-to-many foreign key defined default only on source",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
                "id does not define default but RefSchema.schema_ref_schemas_id does",
            ),
            id="one-to-many foreign key defined default only on referenced",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
                "the default of id must match the default of "
                "RefSchema.schema_ref_schemas_id",
            ),
            id="one-to-many foreign key defined different default",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
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
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "properties": {"schema_ref_schemas_id": {"type": "integer",}},
                }
            },
            (False, "RefSchema.schema_ref_schemas_id must define a foreign key"),
            id="one-to-many foreign key defined no foreign key",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
                "RefSchema.schema_ref_schemas_id must define a foreign key to "
                "Schema.id",
            ),
            id="one-to-many foreign key defined wrong foreign key",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"}},},
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
        pytest.param(
            {"properties": {"id": {"type": "integer", "x-primary-key": True}},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "referenced schema must define x-tablename"),
            id="many-to-many referenced no tablename",
        ),
        pytest.param(
            {
                "x-tablename": True,
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "value of x-tablename must be a string"),
            id="many-to-many referenced invalid tablename",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "referenced schema must define x-tablename"),
            id="many-to-many referenced no tablename",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-secondary": "schema_ref_schema",
                    "x-tablename": True,
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "value of x-tablename must be a string"),
            id="many-to-many referenced invalid tablename",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"type": "integer"},},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "source schema must have a primary key"),
            id="many-to-many source no primary key property",
        ),
        pytest.param(
            {"x-tablename": "schema", "properties": {"id": {"x-primary-key": True},},},
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (False, "id must define a type"),
            id="many-to-many source invalid primary key property",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {
                    "id": {"type": "integer", "x-primary-key": True},
                    "name": {"type": "string", "x-primary-key": True},
                },
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (
                False,
                "many-to-many relationships currently only support single "
                "primary key schemas",
            ),
            id="many-to-many source multiple primary key property",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer"},},
                }
            },
            (False, "referenced schema must have a primary key"),
            id="many-to-many referenced no primary key property",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"x-primary-key": True,},},
                }
            },
            (False, "RefSchema.id must define a type"),
            id="many-to-many referenced invalid primary key property",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True,},
                        "name": {"type": "string", "x-primary-key": True,},
                    },
                }
            },
            (
                False,
                "many-to-many relationships currently only support single "
                "primary key schemas",
            ),
            id="many-to-many referenced multiple primary key property",
        ),
        pytest.param(
            {
                "x-tablename": "schema",
                "properties": {"id": {"type": "integer", "x-primary-key": True}},
            },
            "ref_schemas",
            {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}},
            {
                "RefSchema": {
                    "x-tablename": "ref_schema",
                    "x-secondary": "schema_ref_schema",
                    "properties": {"id": {"type": "integer", "x-primary-key": True,}},
                }
            },
            (True, None),
            id="many-to-many valid",
        ),
    ],
)
@pytest.mark.schemas
def test_check(source_schema, property_name, property_schema, schemas, expected_result):
    """
    GIVEN schemas, the source and property schema and the expected result
    WHEN check is called with the schemas and source and property schema
    THEN the expected result is returned.
    """
    # pylint: disable=assignment-from-no-return
    returned_result = full.check(schemas, source_schema, property_name, property_schema)

    assert returned_result == expected_result
