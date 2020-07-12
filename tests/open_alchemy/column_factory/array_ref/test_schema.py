"""Tests for schema."""
# pylint: disable=protected-access

import pytest

from open_alchemy import types
from open_alchemy.column_factory import array_ref


@pytest.mark.parametrize(
    "artifacts, expected_schema",
    [
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
            ),
            {"type": "array", "items": {"type": "object", "x-de-$ref": "RefSchema"}},
            id="plain",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                description="description 1",
            ),
            {
                "type": "array",
                "items": {"type": "object", "x-de-$ref": "RefSchema"},
                "description": "description 1",
            },
            id="description",
        ),
        pytest.param(
            types.ObjectArtifacts(
                spec={},
                logical_name="logical name 1",
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                write_only=True,
            ),
            {
                "type": "array",
                "items": {"type": "object", "x-de-$ref": "RefSchema"},
                "writeOnly": True,
            },
            id="writeOnly",
        ),
    ],
)
@pytest.mark.column
def test_calculate(artifacts, expected_schema):
    """
    GIVEN array artifacts
    WHEN calculate is called with the artifacts
    THEN the schema for the array reference is returned.
    """
    schema = array_ref._schema.calculate(artifacts=artifacts)

    assert schema == expected_schema
