"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "schema, expected_source",
    [
        (
            {"properties": {"id": {"type": "integer"}}},
            '''

class Model(models.Model):
    """Model SQLAlchemy model."""

    id: typing.Optional[int]''',
        ),
        (
            {"properties": {"id": {"type": "integer"}}, "required": ["id"]},
            '''

class Model(models.Model):
    """Model SQLAlchemy model."""

    id: int''',
        ),
        (
            {"properties": {"id": {"type": "integer"}}, "required": []},
            '''

class Model(models.Model):
    """Model SQLAlchemy model."""

    id: typing.Optional[int]''',
        ),
    ],
    ids=["single property", "single required property", "single not required property"],
)
@pytest.mark.models_file
def test_generate(schema, expected_source):
    """
    GIVEN schema and name
    WHEN generate is called with the schema and name
    THEN the model source code is returned.
    """
    source = models_file._model.generate(schema=schema, name="Model")

    assert source == expected_source
