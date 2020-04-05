"""Tests for prepare_schema helper."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"key": "value"}, {}),
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"key": "value"}}),
        ({"allOf": [{"key": "value"}]}, {}),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"allOf": [{"key": "value"}]}},
        ),
    ],
    ids=["plain", "$ref", "allOf", "$ref then allOf", "allOf with $ref"],
)
@pytest.mark.helper
def test_prepare_schema(schema, schemas):
    """
    GIVEN schema, schemas and expected schema
    WHEN prepare_schema is called with the schema and schemas
    THEN the expected schema is returned.
    """
    returned_schema = helpers.prepare_schema(schema=schema, schemas=schemas)

    assert returned_schema == {"key": "value"}


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"key": "value"}}),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"key": "value"}},
        ),
    ],
    ids=["$ref skip", "allOf skip"],
)
@pytest.mark.helper
def test_prepare_schema_skip(schema, schemas):
    """
    GIVEN schema, schemas
    WHEN prepare_schema is called with the schema and schemas and skip name
    THEN the an empty schema is returned.
    """
    returned_schema = helpers.prepare_schema(
        schema=schema, schemas=schemas, skip_name="RefSchema"
    )

    assert returned_schema == {}
