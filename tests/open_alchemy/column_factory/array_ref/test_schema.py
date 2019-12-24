"""Tests for schema."""
# pylint: disable=protected-access

import pytest

from open_alchemy import types
from open_alchemy.column_factory import array_ref


@pytest.mark.column
def test_calculate():
    """
    GIVEN array artifacts
    WHEN calculate is called with the artifacts
    THEN the schema for the array reference is returned.
    """
    relationship = types.RelationshipArtifacts("RefSchema")
    artifacts = types.ObjectArtifacts(
        spec={}, fk_column="fk_column", relationship=relationship
    )

    schema = array_ref._schema.calculate(artifacts=artifacts)

    assert schema == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }
