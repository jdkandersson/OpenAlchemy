"""Tests for _calculate_schema."""
# pylint: disable=protected-access

import pytest

from open_alchemy import types
from open_alchemy.column_factory import object_ref


@pytest.mark.parametrize(
    "artifacts, expected_schema",
    [
        (
            types.ObjectArtifacts(
                spec={},
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
            ),
            {"type": "object", "x-de-$ref": "RefSchema"},
        ),
        (
            types.ObjectArtifacts(
                spec={},
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                nullable=True,
            ),
            {"type": "object", "x-de-$ref": "RefSchema", "nullable": True},
        ),
        (
            types.ObjectArtifacts(
                spec={},
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                nullable=False,
            ),
            {"type": "object", "x-de-$ref": "RefSchema", "nullable": False},
        ),
        (
            types.ObjectArtifacts(
                spec={},
                fk_column="fk_column",
                relationship=types.RelationshipArtifacts("RefSchema"),
                description="description 1",
            ),
            {
                "type": "object",
                "x-de-$ref": "RefSchema",
                "description": "description 1",
            },
        ),
    ],
    ids=["plain", "nullable True", "nullable False", "description"],
)
@pytest.mark.column
def test_calculate_schema(artifacts, expected_schema):
    """
    GIVEN object reference artifacts
    WHEN _calculate_schema is called with the artifacts
    THEN the calculate for the array reference is returned.
    """
    schema = object_ref._schema.calculate(artifacts=artifacts)

    assert schema == expected_schema
