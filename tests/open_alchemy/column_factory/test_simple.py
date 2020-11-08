"""Tests for the simple column factory."""

import pytest

from open_alchemy import facades
from open_alchemy import types
from open_alchemy.column_factory import simple
from open_alchemy.schemas.artifacts import types as artifacts_types


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    artifacts = artifacts_types.SimplePropertyArtifacts(
        type=types.PropertyType.SIMPLE,
        open_api=artifacts_types.OpenApiSimplePropertyArtifacts(
            type="integer",
            format=None,
            max_length=None,
            nullable=None,
            default=None,
            read_only=None,
            write_only=None,
        ),
        extension=artifacts_types.ExtensionSimplePropertyArtifacts(
            primary_key=None,
            autoincrement=None,
            index=None,
            unique=None,
            server_default=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=None,
        ),
        schema={"type": "integer"},
        required=False,
        description=None,
    )

    returned_column = simple.handle(artifacts=artifacts)

    assert isinstance(returned_column, facades.sqlalchemy.types.Column)
    assert isinstance(returned_column.type, facades.sqlalchemy.types.Integer)
