"""Tests for backref schemas processing."""

import pytest

from open_alchemy import exceptions
from open_alchemy.schemas import backref


@pytest.mark.schemas
def test_process_not_found():
    """
    GIVEN schemas with a back reference that is not found
    WHEN process is called with the schemas
    THEN SchemasNotFoundError is raised.
    """
    schemas = {
        "Schema1": {
            "x-tablename": "schema1",
            "properties": {
                "prop_1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RefSchema1"},
                        {"x-backref": "schema1"},
                    ]
                }
            },
        },
    }
    with pytest.raises(exceptions.SchemaNotFoundError):
        backref.process(schemas=schemas)


@pytest.mark.parametrize(
    "schemas, expected_schemas",
    [
        pytest.param(
            {},
            {},
            id="empty",
        ),
        pytest.param(
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
                        }
                    },
                },
                "RefSchema1": {"ref_key_1": "ref_value 1"},
            },
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [{"$ref": "#/components/schemas/RefSchema1"}]
                        }
                    },
                },
                "RefSchema1": {"ref_key_1": "ref_value 1"},
            },
            id="single no backref",
        ),
        pytest.param(
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    },
                },
                "RefSchema1": {"ref_key_1": "ref_value 1"},
            },
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    },
                },
                "RefSchema1": {
                    "allOf": [
                        {"ref_key_1": "ref_value 1"},
                        {
                            "type": "object",
                            "x-backrefs": {
                                "schema1": {
                                    "type": "array",
                                    "items": {"type": "object", "x-de-$ref": "Schema1"},
                                }
                            },
                        },
                    ]
                },
            },
            id="single backref",
        ),
        pytest.param(
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    },
                },
                "RefSchema1": {"ref_key_1": "ref_value 1"},
                "Schema2": {
                    "x-tablename": "schema2",
                    "properties": {
                        "prop_2": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema2"},
                                {"x-backref": "schema2"},
                            ]
                        }
                    },
                },
                "RefSchema2": {"ref_key_2": "ref_value 2"},
            },
            {
                "Schema1": {
                    "x-tablename": "schema1",
                    "properties": {
                        "prop_1": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema1"},
                                {"x-backref": "schema1"},
                            ]
                        }
                    },
                },
                "RefSchema1": {
                    "allOf": [
                        {"ref_key_1": "ref_value 1"},
                        {
                            "type": "object",
                            "x-backrefs": {
                                "schema1": {
                                    "type": "array",
                                    "items": {"type": "object", "x-de-$ref": "Schema1"},
                                }
                            },
                        },
                    ]
                },
                "Schema2": {
                    "x-tablename": "schema2",
                    "properties": {
                        "prop_2": {
                            "allOf": [
                                {"$ref": "#/components/schemas/RefSchema2"},
                                {"x-backref": "schema2"},
                            ]
                        }
                    },
                },
                "RefSchema2": {
                    "allOf": [
                        {"ref_key_2": "ref_value 2"},
                        {
                            "type": "object",
                            "x-backrefs": {
                                "schema2": {
                                    "type": "array",
                                    "items": {"type": "object", "x-de-$ref": "Schema2"},
                                }
                            },
                        },
                    ]
                },
            },
            id="multiple backref",
        ),
    ],
)
@pytest.mark.schemas
def test_process(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN process is called with the schemas
    THEN the expected schemas are modified so that they are equal to the expected
        schemas.
    """
    backref.process(schemas=schemas)

    assert schemas == expected_schemas
