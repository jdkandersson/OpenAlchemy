"""Tests for prepare_spec helper."""

import pytest

from openapi_sqlalchemy import helpers


@pytest.mark.helper
def test_simple():
    """
    GIVEN specification without any special statements
    WHEN prepare_spec is called
    THEN specification is returned.
    """
    spec = {"key": "value"}
    schemas = {}

    returned_spec = helpers.prepare_spec(spec=spec, schemas=schemas)

    assert returned_spec == {"key": "value"}


@pytest.mark.helper
def test_ref():
    """
    GIVEN specification with $ref and schemas with referenced specification
    WHEN prepare_spec is called
    THEN the referenced specification is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"key": "value"}}

    returned_spec = helpers.prepare_spec(spec=spec, schemas=schemas)

    assert returned_spec == {"key": "value"}


@pytest.mark.helper
def test_all_of():
    """
    GIVEN specification without any special statements
    WHEN prepare_spec is called
    THEN specification is returned.
    """
    spec = {"allOf": [{"key": "value"}]}
    schemas = {}

    returned_spec = helpers.prepare_spec(spec=spec, schemas=schemas)

    assert returned_spec == {"key": "value"}


@pytest.mark.helper
def test_ref_all_of():
    """
    GIVEN specification without any special statements
    WHEN prepare_spec is called
    THEN specification is returned.
    """
    spec = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"allOf": [{"key": "value"}]}}

    returned_spec = helpers.prepare_spec(spec=spec, schemas=schemas)

    assert returned_spec == {"key": "value"}
