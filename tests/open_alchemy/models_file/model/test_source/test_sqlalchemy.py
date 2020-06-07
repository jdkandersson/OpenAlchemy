"""Tests for model source generation."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file

_SQLAlchemyModelArtifacts = models_file.types.SQLAlchemyModelArtifacts
_ArgArtifacts = models_file.types.ArgArtifacts
_ColumnArtifacts = models_file.types.ColumnArtifacts
_ColumnArgArtifacts = models_file.types.ColumnArgArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            _SQLAlchemyModelArtifacts(
                name="Model",
                columns=[],
                empty=True,
                arg=_ArgArtifacts(required=[], not_required=[]),
                parent_cls="Parent",
            ),
            '''

class TModel(Parent):
    """SQLAlchemy model protocol."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    def __init__(self) -> None:
        """Construct."""
        ...

    @classmethod
    def from_dict(cls) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

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


Model: typing.Type[TModel] = models.Model  # type: ignore''',
        ),
        (
            _SQLAlchemyModelArtifacts(
                name="Model",
                columns=[_ColumnArtifacts(name="column_1", type="type_1")],
                empty=False,
                arg=_ArgArtifacts(
                    required=[
                        _ColumnArgArtifacts(
                            name="column_1",
                            init_type="init_type_1",
                            from_dict_type="fd_type_1",
                        )
                    ],
                    not_required=[],
                ),
                parent_cls="Parent",
            ),
            '''

class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        column_1: The column_1 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: 'sqlalchemy.Column[type_1]'

    def __init__(self, column_1: init_type_1) -> None:
        """
        Construct.

        Args:
            column_1: The column_1 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, column_1: fd_type_1) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            column_1: The column_1 of the Model.

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


Model: typing.Type[TModel] = models.Model  # type: ignore''',
        ),
        (
            _SQLAlchemyModelArtifacts(
                name="Model",
                columns=[_ColumnArtifacts(name="column_1", type="type_1")],
                empty=False,
                arg=_ArgArtifacts(
                    required=[
                        _ColumnArgArtifacts(
                            name="column_1",
                            init_type="init_type_1",
                            from_dict_type="fd_type_1",
                            read_only=True,
                        )
                    ],
                    not_required=[],
                ),
                parent_cls="Parent",
            ),
            '''

class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        column_1: The column_1 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: 'sqlalchemy.Column[type_1]'

    def __init__(self, column_1: init_type_1) -> None:
        """
        Construct.

        Args:
            column_1: The column_1 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            column_1: The column_1 of the Model.

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


Model: typing.Type[TModel] = models.Model  # type: ignore''',
        ),
        (
            _SQLAlchemyModelArtifacts(
                name="Model",
                columns=[
                    _ColumnArtifacts(name="column_1", type="type_1"),
                    _ColumnArtifacts(name="column_2", type="type_2"),
                ],
                empty=False,
                arg=_ArgArtifacts(
                    required=[
                        _ColumnArgArtifacts(
                            name="column_1",
                            init_type="init_type_1",
                            from_dict_type="fd_type_1",
                        ),
                        _ColumnArgArtifacts(
                            name="column_2",
                            init_type="init_type_2",
                            from_dict_type="fd_type_2",
                        ),
                    ],
                    not_required=[],
                ),
                parent_cls="Parent",
            ),
            '''

class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        column_1: The column_1 of the Model.
        column_2: The column_2 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: 'sqlalchemy.Column[type_1]'
    column_2: 'sqlalchemy.Column[type_2]'

    def __init__(self, column_1: init_type_1, column_2: init_type_2) -> None:
        """
        Construct.

        Args:
            column_1: The column_1 of the Model.
            column_2: The column_2 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, column_1: fd_type_1, column_2: fd_type_2) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            column_1: The column_1 of the Model.
            column_2: The column_2 of the Model.

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


Model: typing.Type[TModel] = models.Model  # type: ignore''',
        ),
    ],
    ids=["empty", "single column", "single column readOnly", "multiple column"],
)
@pytest.mark.models_file
def test_sqlalchemy(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN sqlalchemy is called with the artifacts
    THEN the source code for the model class is returned.
    """
    source = models_file._model._source.sqlalchemy(artifacts=artifacts)

    assert source == expected_source
