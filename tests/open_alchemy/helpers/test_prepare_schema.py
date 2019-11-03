"""Tests for prepare_schema helper."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_schema",
    [
        ({"key": "value"}, {}, {"key": "value"}),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"key": "value"}},
            {"key": "value"},
        ),
        ({"allOf": [{"key": "value"}]}, {}, {"key": "value"}),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
            {"key": "value"},
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
            {"key": "value"},
        ),
    ],
    ids=["plain", "$ref", "allOf", "$ref then allOf", "allOf with $ref"],
)
@pytest.mark.helper
def test_prepare_schema(schema, schemas, expected_schema):
    """
    GIVEN schema, schemas and expected schema
    WHEN prepare_schema is called with the schema and schemas
    THEN the expected schema is returned.
    """
    returned_schema = helpers.prepare_schema(schema=schema, schemas=schemas)

    assert returned_schema == expected_schema
