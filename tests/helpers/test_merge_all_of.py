"""Tests for merge allOf helper."""


import pytest

from openapi_sqlalchemy import helpers


@pytest.mark.helper
def test_not_all_of():
    """
    GIVEN schema that does not have the allOf statement
    WHEN merge_all_of is called with the schema
    THEN the schema is returned.
    """
    schema = {"key": "value"}

    return_schema = helpers.merge_all_of(schema=schema)

    assert return_schema == {"key": "value"}


@pytest.mark.helper
def test_all_of_single():
    """
    GIVEN schema that does not have the allOf statement
    WHEN merge_all_of is called with the schema
    THEN the schema is returned.
    """
    schema = {"allOf": [{"key": "value"}]}

    return_schema = helpers.merge_all_of(schema=schema)

    assert return_schema == {"key": "value"}
