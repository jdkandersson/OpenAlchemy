"""Tests for resolve_ref."""

import pytest

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import helpers


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
    return_schema = helpers.resolve_ref(schema={"type": "integer"}, schemas={})

    assert return_schema == {"type": "integer"}


def test_resolve_ref_not_schema():
    """
    GIVEN schema that references something that is not a schema
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/not/schema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(schema=schema, schemas=schemas)


def test_resolve_ref_not_defined():
    """
    GIVEN schema that references a schema that doesn't exist
    WHEN resolve_ref is called with the schema
    THEN SchemaNotFoundError is raised.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        helpers.resolve_ref(schema=schema, schemas=schemas)
