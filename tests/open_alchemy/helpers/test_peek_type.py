"""Tests for peek_type helper."""

import pytest

from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({}, {}),
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"key": "value"}}),
        ({"allOf": [{"key": "value"}]}, {}),
    ],
    ids=["plain", "$ref", "allOf"],
)
@pytest.mark.helper
def test_peek_type_no_type(schema, schemas):
    """
    GIVEN schema without a type
    WHEN peek_type is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        helpers.peek_type(schema=schema, schemas=schemas)


@pytest.mark.parametrize(
    "schema, schemas, expected_type",
    [
        ({"type": "type 1"}, {}, "type 1"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "type 1"}},
            "type 1",
        ),
        ({"allOf": [{"type": "type 1"}]}, {}, "type 1"),
        ({"allOf": [{"type": "type 1"}, {"type": "type 2"}]}, {}, "type 1"),
        ({"allOf": [{"key": "value"}, {"type": "type 2"}]}, {}, "type 2"),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"type": "type 1"}]}},
            "type 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"type": "type 1"}]}},
            "type 1",
        ),
    ],
    ids=[
        "plain",
        "$ref",
        "allOf single",
        "allOf multiple first",
        "allOf multiple last",
        "$ref then allOf",
        "allOf with $ref",
    ],
)
@pytest.mark.helper
def test_peek_type(schema, schemas, expected_type):
    """
    GIVEN schema, schemas and expected type
    WHEN peek_type is called with the schema and schemas
    THEN the expected type is returned.
    """
    returned_type = helpers.peek_type(schema=schema, schemas=schemas)

    assert returned_type == expected_type
