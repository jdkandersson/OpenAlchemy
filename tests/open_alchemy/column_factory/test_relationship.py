"""Tests for the relationship column factory."""

import pytest

from open_alchemy import types
from open_alchemy.column_factory import relationship
from open_alchemy.schemas.artifacts import types as artifacts_types


@pytest.mark.column
def test_handle():
    """
    GIVEN schema that references another object schema and schemas
    WHEN handle is called with the schema and schemas
    THEN relationship is returned with the spec.
    """
    artifacts = artifacts_types.ManyToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={"key": "value"},
        required=False,
        description=None,
        sub_type=types.RelationshipType.MANY_TO_ONE,
        parent="Parent",
        backref_property=None,
        kwargs=None,
        write_only=False,
        foreign_key_property="prop_1",
        foreign_key="foreign.key",
        nullable=False,
    )
    logical_name = "ref_schema"

    (
        [(returned_logical_name, returned_relationship)],
        returned_schema,
    ) = relationship.handle(
        artifacts=artifacts,
        logical_name=logical_name,
    )

    assert returned_logical_name == logical_name
    assert returned_relationship.argument == "Parent"
    assert returned_relationship.backref is None
    assert returned_relationship.uselist is None
    assert returned_schema == {"key": "value"}
