"""Tests for _calculate_schema."""
# pylint: disable=protected-access

import pytest

from open_alchemy import types
from open_alchemy.column_factory import object_ref


@pytest.mark.column
def test_calculate_schema():
    """
    GIVEN array artifacts
    WHEN _calculate_schema is called with the artifacts
    THEN the schema for the array reference is returned.
    """
    relationship = types.RelationshipArtifacts("RefSchema")
    artifacts = types.ObjectArtifacts(
        spec={}, fk_column="fk_column", relationship=relationship
    )

    schema = object_ref._calculate_schema.calculate_schema(artifacts=artifacts)

    assert schema == {"type": "object", "x-de-$ref": "RefSchema"}
