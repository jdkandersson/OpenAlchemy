"""Tests for resolve_ref."""

import copy

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.helper
def test_resolve_ref_exists():
    """
    GIVEN
    WHEN
    THEN helpers has resolve_ref property.
    """
    assert hasattr(helpers, "resolve_ref")


@pytest.mark.helper
def test_resolve_ref_not_ref_schema():
    """
    GIVEN schema that does not have $ref and name
    WHEN resolve_ref is called with the schema and name
    THEN the schema and name are returned.
    """
    name = "name 1"
    schema = {"type": "integer"}
    schemas = {}

    (return_name, return_schema) = helpers.resolve_ref(
        name=name, schema=copy.deepcopy(schema), schemas=schemas
    )

    assert return_name == name
    assert return_schema == schema


@pytest.mark.helper
def test_resolve_ref_not_schema():
    """
    GIVEN schema that references something that is not a schema
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/not/schema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(name="name 1", schema=schema, schemas=schemas)


@pytest.mark.helper
def test_resolve_ref_not_defined():
    """
    GIVEN schema that references a schema that doesn't exist
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(name="name 1", schema=schema, schemas=schemas)


@pytest.mark.helper
def test_resolve_ref_single():
    """
    GIVEN schema that references another schema and schemas
    WHEN resolve_ref is called with the schema and schemas
    THEN the referenced schema and logical name is returned.
    """
    ref_schema = {"type": "boolean"}
    ref_name = "RefSchema"
    schema = {"$ref": f"#/components/schemas/{ref_name}"}
    schemas = {ref_name: copy.deepcopy(ref_schema)}

    (return_name, return_schema) = helpers.resolve_ref(
        name="name 1", schema=schema, schemas=schemas
    )

    assert return_name == ref_name
    assert return_schema == ref_schema


@pytest.mark.helper
def test_resolve_ref_nested():
    """
    GIVEN schema that references another schema which also references another schema
        and schemas
    WHEN resolve_ref is called with the schema and schemas
    THEN the final referenced schema and logical name is returned.
    """
    ref_schema = {"type": "boolean"}
    ref_name = "RefSchema"
    schema = {"$ref": "#/components/schemas/NestedRefSchema"}
    schemas = {
        "NestedRefSchema": {"$ref": f"#/components/schemas/{ref_name}"},
        "RefSchema": copy.deepcopy(ref_schema),
    }

    (return_name, return_schema) = helpers.resolve_ref(
        name="name 1", schema=schema, schemas=schemas
    )

    assert return_name == ref_name
    assert return_schema == ref_schema
