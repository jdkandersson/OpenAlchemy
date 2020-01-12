"""Tests for model."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file

_EXPECTED_TD_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_TD_BASE = "typing_extensions.TypedDict"
_EXPECTED_MODEL_BASE = "typing.Protocol"
if sys.version_info[1] < 8:
    _EXPECTED_MODEL_BASE = "typing_extensions.Protocol"


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

class ModelDict({_EXPECTED_TD_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]


class TModel({_EXPECTED_MODEL_BASE}):
    """SQLAlchemy model protocol."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: typing.Optional[int]

    def __init__(self, id: typing.Optional[int] = None) -> None:
        """Construct."""
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None) -> "TModel":
        """Construct from a dictionary (eg. a POST payload)."""
        ...

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        ...


Model: TModel = models.Model  # type: ignore'''

    assert source == expected_source
