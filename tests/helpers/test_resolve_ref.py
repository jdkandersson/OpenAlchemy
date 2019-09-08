"""Tests for resolve_ref."""

import pytest

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import helpers
from openapi_sqlalchemy import types


@pytest.mark.helper
def test_resolve_ref_exists():
    """
    GIVEN
    WHEN
    THEN helpers has resolve_ref property.
    """
    assert hasattr(helpers, "resolve_ref")


def test_resolve_ref_not_ref_schema():
    """
    GIVEN schema that does not have $ref
    WHEN resolve_ref is called with the schema
    THEN the schema is returned.
    """
    schema = types.Schema("Schema", {"type": "integer"})
    schemas = {}

    return_schema = helpers.resolve_ref(schema=schema, schemas=schemas)

    expected_schema = types.Schema("Schema", {"type": "integer"})
    assert return_schema == expected_schema


def test_resolve_ref_not_schema():
    """
    GIVEN schema that references something that is not a schema
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = types.Schema("Schema", {"$ref": "#/components/not/schema"})
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(schema=schema, schemas=schemas)


def test_resolve_ref_not_defined():
    """
    GIVEN schema that references a schema that doesn't exist
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = types.Schema("Schema", {"$ref": "#/components/schemas/RefSchema"})
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(schema=schema, schemas=schemas)


def test_resolve_ref_single():
    """
    GIVEN schema that references another schema and schemas
    WHEN resolve_ref is called with the schema and schemas
    THEN the referenced schema and logical name is returned.
    """
    schema = types.Schema("Schema", {"$ref": "#/components/schemas/RefSchema"})
    schemas = {"RefSchema": {"type": "boolean"}}

    return_schema = helpers.resolve_ref(schema=schema, schemas=schemas)

    expected_schema = types.Schema("RefSchema", {"type": "boolean"})
    assert return_schema == expected_schema


def test_resolve_ref_nested():
    """
    GIVEN schema that references another schema which also references another schema
        and schemas
    WHEN resolve_ref is called with the schema and schemas
    THEN the final referenced schema and logical name is returned.
    """
    schema = types.Schema("Schema", {"$ref": "#/components/schemas/NestedRefSchema"})
    schemas = {
        "NestedRefSchema": {"$ref": "#/components/schemas/RefSchema"},
        "RefSchema": {"type": "boolean"},
    }

    return_schema = helpers.resolve_ref(schema=schema, schemas=schemas)

    expected_schema = types.Schema("RefSchema", {"type": "boolean"})
    assert return_schema == expected_schema
