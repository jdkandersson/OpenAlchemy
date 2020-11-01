"""Tests for the column factory."""

import pytest

from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy.column_factory import simple
from open_alchemy.schemas.artifacts import types as artifacts_types


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle_column is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    artifacts = artifacts_types.SimplePropertyArtifacts(
        type=helpers.property_.Type.SIMPLE,
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
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
            dict_ignore=None,
        ),
        schema={"type": "integer"},
        required=False,
        description=None,
    )

    returned_column, returned_schema = simple.handle(artifacts=artifacts)

    assert isinstance(returned_column, facades.sqlalchemy.column.Column)
    assert isinstance(returned_column.type, facades.sqlalchemy.column.Integer)
    assert returned_schema == {"type": "integer"}
