"""Tests for the column factory."""

import pytest

from open_alchemy import column_factory
from open_alchemy import facades
from open_alchemy import types


@pytest.mark.column
def test_integration_simple():
    """
    GIVEN simple column artifacts
    WHEN column_factory is called with the artifacts
    THEN a SQLAlchemy boolean column is returned.
    """
    artifacts = types.SimplePropertyArtifacts(
        type=types.PropertyType.SIMPLE,
        open_api=types.OpenApiSimplePropertyArtifacts(
            type="boolean",
            format=None,
            max_length=None,
            nullable=None,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=types.ExtensionSimplePropertyArtifacts(
            primary_key=False,
            autoincrement=None,
            index=None,
            unique=None,
            server_default=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=False,
        ),
        schema={"type": "boolean"},
        required=False,
        description=None,
    )

    column = column_factory.column_factory(artifacts=artifacts)

    assert isinstance(column, facades.sqlalchemy.types.Column)
    assert isinstance(column.type, facades.sqlalchemy.types.Boolean)


@pytest.mark.column
def test_integration_json():
    """
    GIVEN json column artifacts
    WHEN column_factory is called with the artifacts
    THEN a SQLAlchemy JSON column is returned.
    """
    artifacts = types.JsonPropertyArtifacts(
        type=types.PropertyType.JSON,
        open_api=types.OpenApiJsonPropertyArtifacts(
            nullable=None,
            read_only=None,
            write_only=None,
        ),
        extension=types.ExtensionJsonPropertyArtifacts(
            primary_key=False,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
        ),
        schema={"type": "boolean"},
        required=False,
        description=None,
    )

    column = column_factory.column_factory(artifacts=artifacts)

    assert isinstance(column, facades.sqlalchemy.types.Column)
    assert isinstance(column.type, facades.sqlalchemy.types.JSON)


@pytest.mark.column
def test_integration_relationship():
    """
    GIVEN relationship property artifacts
    WHEN column_factory is called with the artifacts
    THEN a relationship is returned.
    """
    artifacts = types.ManyToOneRelationshipPropertyArtifacts(
        type=types.PropertyType.RELATIONSHIP,
        sub_type=types.RelationshipType.MANY_TO_ONE,
        parent="RefSchema",
        backref_property=None,
        kwargs=None,
        write_only=None,
        description=None,
        required=False,
        schema={"type": "object"},
        foreign_key="foreign.key",
        foreign_key_property="foreign_key",
        nullable=None,
    )

    relationship = column_factory.column_factory(artifacts=artifacts)

    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.uselist is None


@pytest.mark.column
def test_integration_backref():
    """
    GIVEN backref property artifacts
    WHEN column_factory is called with the artifacts
    THEN None is returned.
    """
    artifacts = types.BackrefPropertyArtifacts(
        type=types.PropertyType.BACKREF,
        sub_type=types.BackrefSubType.OBJECT,
        properties=[],
        schema={},
        required=None,
        description=None,
    )

    backref = column_factory.column_factory(artifacts=artifacts)

    assert backref is None
