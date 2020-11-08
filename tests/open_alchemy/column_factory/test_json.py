"""Tests for the json column factory."""

import pytest

from open_alchemy import facades
from open_alchemy import types
from open_alchemy.column_factory import json
from open_alchemy.schemas.artifacts import types as artifacts_types


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    artifacts = artifacts_types.JsonPropertyArtifacts(
        type=types.PropertyType.JSON,
        open_api=artifacts_types.OpenApiJsonPropertyArtifacts(
            nullable=None,
            read_only=None,
            write_only=None,
        ),
        extension=artifacts_types.ExtensionJsonPropertyArtifacts(
            primary_key=None,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
        ),
        schema={"type": "integer"},
        required=False,
        description=None,
    )

    returned_column = json.handle(artifacts=artifacts)

    assert isinstance(returned_column, facades.sqlalchemy.types.Column)
    assert isinstance(returned_column.type, facades.sqlalchemy.types.JSON)
