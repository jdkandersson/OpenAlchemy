"""Tests for read_only handling."""

import pytest

from open_alchemy import types as oa_types
from open_alchemy.column_factory import backref
from open_alchemy.schemas.artifacts import types


@pytest.mark.column
def test_handle():
    """
    GIVEN artifacts
    WHEN handle is called
    THEN the schema from the artifacts is returned.
    """
    artifacts = types.BackrefPropertyArtifacts(
        type=oa_types.PropertyType.BACKREF,
        schema={"key": "value"},
        required=None,
        description=None,
        sub_type=types.BackrefSubType.OBJECT,
        properties=[],
    )

    returned_columns, returned_schema = backref.handle(artifacts=artifacts)

    assert returned_columns == []
    assert returned_schema == {"key": "value"}
