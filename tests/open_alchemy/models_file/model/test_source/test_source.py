"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file

_SQLAlchemyModelArtifacts = models_file.types.SQLAlchemyModelArtifacts
_ArgArtifacts = models_file.types.ArgArtifacts
_ColumnArtifacts = models_file.types.ColumnArtifacts
_ColumnArgArtifacts = models_file.types.ColumnArgArtifacts
_TypedDictArtifacts = models_file.types.TypedDictArtifacts
_TypedDictClassArtifacts = models_file.types.TypedDictClassArtifacts
_ModelArtifacts = models_file.types.ModelArtifacts


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            _ModelArtifacts(
                sqlalchemy=_SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[],
                    empty=True,
                    arg=_ArgArtifacts(required=[], not_required=[]),
                    parent_cls="Parent",
                ),
                typed_dict=_TypedDictArtifacts(
                    required=_TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                    not_required=_TypedDictClassArtifacts(
                        props=[],
                        empty=True,
                        name="ModelDict",
                        parent_class="typing.TypedDict",
                    ),
                ),
            ),
            '''

class ModelDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""


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
            _ModelArtifacts(
                sqlalchemy=_SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[_ColumnArtifacts(name="col_1", type="model_type_1")],
                    empty=False,
                    arg=_ArgArtifacts(
                        required=[],
                        not_required=[
                            _ColumnArgArtifacts(
                                name="col_1",
                                init_type="arg_i_type_1",
                                from_dict_type="arg_fd_type_1",
                            )
                        ],
                    ),
                    parent_cls="Parent",
                ),
                typed_dict=_TypedDictArtifacts(
                    required=_TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                    not_required=_TypedDictClassArtifacts(
                        props=[_ColumnArtifacts(name="col_1", type="td_type_1")],
                        empty=False,
                        name="ModelDict",
                        parent_class="typing.TypedDict",
                    ),
                ),
            ),
            '''

class ModelDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    col_1: td_type_1


class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        col_1: The col_1 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: 'sqlalchemy.Column[model_type_1]'

    def __init__(self, col_1: arg_i_type_1 = None) -> None:
        """
        Construct.

        Args:
            col_1: The col_1 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1 = None) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            col_1: The col_1 of the Model.

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
            _ModelArtifacts(
                sqlalchemy=_SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[_ColumnArtifacts(name="col_1", type="model_type_1")],
                    empty=False,
                    arg=_ArgArtifacts(
                        required=[
                            _ColumnArgArtifacts(
                                name="col_1",
                                init_type="arg_i_type_1",
                                from_dict_type="arg_fd_type_1",
                            )
                        ],
                        not_required=[],
                    ),
                    parent_cls="Parent",
                ),
                typed_dict=_TypedDictArtifacts(
                    required=_TypedDictClassArtifacts(
                        props=[_ColumnArtifacts(name="col_1", type="td_type_1")],
                        empty=False,
                        name="ModelDict",
                        parent_class="typing.TypedDict",
                    ),
                    not_required=_TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                ),
            ),
            '''

class ModelDict(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    col_1: td_type_1


class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        col_1: The col_1 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: 'sqlalchemy.Column[model_type_1]'

    def __init__(self, col_1: arg_i_type_1) -> None:
        """
        Construct.

        Args:
            col_1: The col_1 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            col_1: The col_1 of the Model.

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
            _ModelArtifacts(
                sqlalchemy=_SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        _ColumnArtifacts(name="col_1", type="model_type_1"),
                        _ColumnArtifacts(name="col_2", type="model_type_2"),
                    ],
                    empty=False,
                    arg=_ArgArtifacts(
                        required=[
                            _ColumnArgArtifacts(
                                name="col_1",
                                init_type="arg_i_type_1",
                                from_dict_type="arg_fd_type_1",
                            )
                        ],
                        not_required=[
                            _ColumnArgArtifacts(
                                name="col_2",
                                init_type="arg_i_type_2",
                                from_dict_type="arg_fd_type_2",
                            )
                        ],
                    ),
                    parent_cls="Parent",
                ),
                typed_dict=_TypedDictArtifacts(
                    required=_TypedDictClassArtifacts(
                        props=[_ColumnArtifacts(name="col_1", type="td_type_1")],
                        empty=False,
                        name="_ModelDictBase",
                        parent_class="typing.TypedDict",
                    ),
                    not_required=_TypedDictClassArtifacts(
                        props=[_ColumnArtifacts(name="col_2", type="td_type_2")],
                        empty=False,
                        name="ModelDict",
                        parent_class="_ModelDictBase",
                    ),
                ),
            ),
            '''

class _ModelDictBase(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    col_1: td_type_1


class ModelDict(_ModelDictBase, total=False):
    """TypedDict for properties that are not required."""

    col_2: td_type_2


class TModel(Parent):
    """
    SQLAlchemy model protocol.

    Attrs:
        col_1: The col_1 of the Model.
        col_2: The col_2 of the Model.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: 'sqlalchemy.Column[model_type_1]'
    col_2: 'sqlalchemy.Column[model_type_2]'

    def __init__(self, col_1: arg_i_type_1, col_2: arg_i_type_2 = None) -> None:
        """
        Construct.

        Args:
            col_1: The col_1 of the Model.
            col_2: The col_2 of the Model.

        """
        ...

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1, col_2: arg_fd_type_2 = None) -> "TModel":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            col_1: The col_1 of the Model.
            col_2: The col_2 of the Model.

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
    ids=["empty", "required empty", "not required empty", "full"],
)
@pytest.mark.models_file
def test_generate(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN generate is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.generate(artifacts=artifacts)

    assert source == expected_source
