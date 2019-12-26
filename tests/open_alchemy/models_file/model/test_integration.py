"""Tests for model."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file

_EXPECTED_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_BASE = "typing_extensions.TypedDict"


@pytest.mark.models_file
def test_generate():
    """
    GIVEN schema and name
    WHEN generate is called with the schema and name
    THEN the model source code is returned.
    """
    schema = {"properties": {"id": {"type": "integer"}}}

    source = models_file._model.generate(schema=schema, name="Model")

    expected_source = f'''

class ModelDict({_EXPECTED_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]


class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: typing.Optional[int]

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()'''

    assert source == expected_source
