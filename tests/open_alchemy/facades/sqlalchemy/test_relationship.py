"""Tests for SQLAlchemy relationship property facade."""


import pytest

from open_alchemy import types
from open_alchemy.facades.sqlalchemy import relationship
from open_alchemy.schemas.artifacts import types as artifacts_types


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_many_to_one():
    """
    GIVEN artifacts for a many to one relationship
    WHEN construct is called with the artifacts
    THEN a many to one relationship is returned.
    """
    artifacts = artifacts_types.ManyToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={},
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

    returned_relationship = relationship.construct(artifacts=artifacts)

    assert returned_relationship.argument == "Parent"
    assert returned_relationship.backref is None
    assert returned_relationship.secondary is None


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_many_to_one_backref():
    """
    GIVEN artifacts for a many to one relationship with backref
    WHEN construct is called with the artifacts
    THEN a many to one relationship with backref is returned.
    """
    artifacts = artifacts_types.ManyToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={},
        required=False,
        description=None,
        sub_type=types.RelationshipType.MANY_TO_ONE,
        parent="Parent",
        backref_property="prop_1",
        kwargs=None,
        write_only=False,
        foreign_key_property="prop_1",
        foreign_key="foreign.key",
        nullable=False,
    )

    returned_relationship = relationship.construct(artifacts=artifacts)

    assert returned_relationship.backref == ("prop_1", {"uselist": None})


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_many_to_one_kwargs():
    """
    GIVEN artifacts for a many to one relationship with kwargs
    WHEN construct is called with the artifacts
    THEN a many to one relationship with kwargs is returned.
    """
    artifacts = artifacts_types.ManyToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={},
        required=False,
        description=None,
        sub_type=types.RelationshipType.MANY_TO_ONE,
        parent="Parent",
        backref_property=None,
        kwargs={"order_by": "id"},
        write_only=False,
        foreign_key_property="prop_1",
        foreign_key="foreign.key",
        nullable=False,
    )

    returned_relationship = relationship.construct(artifacts=artifacts)

    assert returned_relationship.order_by == "id"


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_one_to_one_backref():
    """
    GIVEN artifacts for a one to one relationship with backref
    WHEN construct is called with the artifacts
    THEN a one to one relationship with backref is returned.
    """
    artifacts = artifacts_types.OneToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={},
        required=False,
        description=None,
        sub_type=types.RelationshipType.ONE_TO_ONE,
        parent="Parent",
        backref_property="prop_1",
        kwargs=None,
        write_only=False,
        foreign_key_property="prop_1",
        foreign_key="foreign.key",
        nullable=False,
    )

    returned_relationship = relationship.construct(artifacts=artifacts)

    assert returned_relationship.backref == ("prop_1", {"uselist": False})


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_many_to_many():
    """
    GIVEN artifacts for a many to many relationship
    WHEN construct is called with the artifacts
    THEN a many to many relationship is returned.
    """
    artifacts = artifacts_types.ManyToManyRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        schema={},
        required=False,
        description=None,
        sub_type=types.RelationshipType.MANY_TO_MANY,
        parent="Parent",
        backref_property=None,
        kwargs=None,
        write_only=False,
        secondary="association",
    )

    returned_relationship = relationship.construct(artifacts=artifacts)

    assert returned_relationship.secondary == "association"
