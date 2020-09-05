"""Tests for model."""
# pylint: disable=protected-access

import sys

import pytest

from open_alchemy import models_file
from open_alchemy.schemas import artifacts as schemas_artifacts
from open_alchemy.schemas import helpers

_EXPECTED_TD_BASE = "typing.TypedDict"
if sys.version_info[1] < 8:
    _EXPECTED_TD_BASE = "typing_extensions.TypedDict"
_EXPECTED_MODEL_BASE = "typing.Protocol"
if sys.version_info[1] < 8:
    _EXPECTED_MODEL_BASE = "typing_extensions.Protocol"


@pytest.mark.models_file
def test_generate():
    """
    GIVEN artifacts and name
    WHEN generate is called with the artifacts and name
    THEN the model source code is returned.
    """
    artifacts = schemas_artifacts.types.ModelArtifacts(
        tablename="table 1",
        inherits=None,
        parent=None,
        description=None,
        mixins=None,
        kwargs=None,
        composite_index=None,
        composite_unique=None,
        backrefs=[],
        properties=[
            (
                "id",
                schemas_artifacts.types.SimplePropertyArtifacts(
                    type=helpers.property_.type_.Type.SIMPLE,
                    open_api=schemas_artifacts.types.OpenApiSimplePropertyArtifacts(
                        type="integer",
                        format=None,
                        max_length=None,
                        nullable=None,
                        default=None,
                        read_only=None,
                        write_only=None,
                    ),
                    extension=schemas_artifacts.types.ExtensionSimplePropertyArtifacts(
                        primary_key=False,
                        autoincrement=None,
                        index=None,
                        unique=None,
                        foreign_key=None,
                        kwargs=None,
                        foreign_key_kwargs=None,
                        dict_ignore=None,
                    ),
                    schema={},  # type: ignore
                    required=False,
                    description=None,
                ),
            )
        ],
    )

    source = models_file._model.generate(artifacts=artifacts, name="Model")

    expected_source = f'''

class ModelDict({_EXPECTED_TD_BASE}, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]


class TModel({_EXPECTED_MODEL_BASE}):
    """
    SQLAlchemy model protocol.

    Attrs:
        id: The id of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[int]]'

    def __init__(self, id: typing.Optional[int] = None) -> None:
        """
        Construct.

        Args:
            id: The id of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: The id of the Model.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TModel":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> ModelDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Model: typing.Type[TModel] = models.Model  # type: ignore'''

    assert source == expected_source
