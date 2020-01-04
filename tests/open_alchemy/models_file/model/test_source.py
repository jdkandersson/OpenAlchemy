"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.SQLAlchemyModelArtifacts(
                name="Model", columns=[], empty=True
            ),
            '''

class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
        (
            models_file.types.SQLAlchemyModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
                empty=False,
            ),
            '''

class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: type_1

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
        (
            models_file.types.SQLAlchemyModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
                empty=False,
            ),
            '''

class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: type_1
    column_2: type_2

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
    ],
    ids=["empty", "single column", "multiple column"],
)
@pytest.mark.only_this
@pytest.mark.models_file
def test_sqlalchemy(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN sqlalchemy is called with the artifacts
    THEN the source code for the model class is returned.
    """
    source = models_file._model._source.sqlalchemy(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.TypedDictArtifacts(
                required=models_file.types.TypedDictClassArtifacts(
                    props=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        )
                    ],
                    empty=False,
                    name="ModelRequiredDict",
                    parent_class="RequiredParentClass",
                ),
                not_required=None,  # type: ignore
            ),
            '''

class ModelRequiredDict(RequiredParentClass, total=True):
    """TypedDict for properties that are required."""

    column_1: type_1''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                required=models_file.types.TypedDictClassArtifacts(
                    props=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        ),
                        models_file.types.ColumnArtifacts(
                            name="column_2", type="type_2"
                        ),
                    ],
                    empty=False,
                    name="ModelRequiredDict",
                    parent_class="RequiredParentClass",
                ),
                not_required=None,  # type: ignore
            ),
            '''

class ModelRequiredDict(RequiredParentClass, total=True):
    """TypedDict for properties that are required."""

    column_1: type_1
    column_2: type_2''',
        ),
    ],
    ids=["single property", "multiple properties"],
)
@pytest.mark.models_file
def test_typed_dict_required(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN typed_dict_required is called with the artifacts
    THEN the source code for the typed dict class is returned.
    """
    source = models_file._model._source.typed_dict_required(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=models_file.types.TypedDictClassArtifacts(
                    props=[],
                    empty=True,
                    name="ModelNotRequiredDict",
                    parent_class="NotRequiredParentClass",
                ),
            ),
            '''

class ModelNotRequiredDict(NotRequiredParentClass, total=False):
    """TypedDict for properties that are not required."""''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=models_file.types.TypedDictClassArtifacts(
                    props=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        )
                    ],
                    empty=False,
                    name="ModelNotRequiredDict",
                    parent_class="NotRequiredParentClass",
                ),
            ),
            '''

class ModelNotRequiredDict(NotRequiredParentClass, total=False):
    """TypedDict for properties that are not required."""

    column_1: type_1''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=models_file.types.TypedDictClassArtifacts(
                    props=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        ),
                        models_file.types.ColumnArtifacts(
                            name="column_2", type="type_2"
                        ),
                    ],
                    empty=False,
                    name="ModelNotRequiredDict",
                    parent_class="NotRequiredParentClass",
                ),
            ),
            '''

class ModelNotRequiredDict(NotRequiredParentClass, total=False):
    """TypedDict for properties that are not required."""

    column_1: type_1
    column_2: type_2''',
        ),
    ],
    ids=["empty", "single property", "multiple properties"],
)
@pytest.mark.models_file
def test_typed_dict_not_required(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN typed_dict_not_required is called with the artifacts
    THEN the source code for the typed dict class is returned.
    """
    source = models_file._model._source.typed_dict_not_required(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (models_file.types.ArgArtifacts(required=[], not_required=[]), ""),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
                not_required=[],
            ),
            ", column_1: type_1",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
            ),
            ", column_1: type_1 = None",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
                not_required=[],
            ),
            ", column_1: type_1, column_2: type_2",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2")
                ],
            ),
            ", column_1: type_1, column_2: type_2 = None",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
            ),
            ", column_1: type_1 = None, column_2: type_2 = None",
        ),
    ],
    ids=[
        "empty",
        "single required",
        "single not required",
        "multiple required",
        "multiple required and not required",
        "multiple not required",
    ],
)
@pytest.mark.models_file
def test_arg_input(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_input is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_input(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (models_file.types.ArgArtifacts(required=[], not_required=[]), "kwargs = {}"),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
                not_required=[],
            ),
            'kwargs = {"column_1": column_1}',
        ),
        (
            models_file.types.ArgArtifacts(
                required=[],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
            ),
            """kwargs = {}
        if column_1 is not None:
            kwargs["column_1"] = column_1""",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
                not_required=[],
            ),
            'kwargs = {"column_1": column_1, "column_2": column_2}',
        ),
        (
            models_file.types.ArgArtifacts(
                required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2")
                ],
            ),
            """kwargs = {"column_1": column_1}
        if column_2 is not None:
            kwargs["column_2"] = column_2""",
        ),
        (
            models_file.types.ArgArtifacts(
                required=[],
                not_required=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
            ),
            """kwargs = {}
        if column_1 is not None:
            kwargs["column_1"] = column_1
        if column_2 is not None:
            kwargs["column_2"] = column_2""",
        ),
    ],
    ids=[
        "empty",
        "single required",
        "single not required",
        "multiple required",
        "multiple required and not required",
        "multiple not required",
    ],
)
@pytest.mark.models_file
def test_arg_kwargs(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_kwargs is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_kwargs(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[],
                    empty=True,
                    arg=models_file.types.ArgArtifacts(required=[], not_required=[]),
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
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


class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    def __init__(self) -> None:
        """Construct."""
        kwargs = {}

        return super().__init__(**kwargs)

    @classmethod
    def from_dict(cls) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {}

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
        (
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="model_type_1"
                        )
                    ],
                    empty=False,
                    arg=models_file.types.ArgArtifacts(
                        required=[],
                        not_required=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="arg_type_1"
                            )
                        ],
                    ),
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="td_type_1"
                            )
                        ],
                        empty=False,
                        name="ModelDict",
                        parent_class="typing.TypedDict",
                    ),
                ),
            ),
            '''

class ModelDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    column_1: td_type_1


class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: model_type_1

    def __init__(self, , column_1: arg_type_1 = None) -> None:
        """Construct."""
        kwargs = {}
        if column_1 is not None:
            kwargs["column_1"] = column_1

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, column_1: arg_type_1 = None) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {}
        if column_1 is not None:
            kwargs["column_1"] = column_1

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
        (
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="model_type_1"
                        )
                    ],
                    empty=False,
                    arg=models_file.types.ArgArtifacts(
                        required=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="arg_type_1"
                            )
                        ],
                        not_required=[],
                    ),
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="td_type_1"
                            )
                        ],
                        empty=False,
                        name="ModelDict",
                        parent_class="typing.TypedDict",
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                ),
            ),
            '''

class ModelDict(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    column_1: td_type_1


class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: model_type_1

    def __init__(self, column_1: arg_type_1) -> None:
        """Construct."""
        kwargs = {"column_1": column_1}

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, column_1: arg_type_1) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"column_1": column_1}

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
        ),
        (
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="model_type_1"
                        ),
                        models_file.types.ColumnArtifacts(
                            name="column_2", type="model_type_2"
                        ),
                    ],
                    empty=False,
                    arg=models_file.types.ArgArtifacts(
                        required=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="arg_type_1"
                            )
                        ],
                        not_required=[
                            models_file.types.ColumnArtifacts(
                                name="column_2", type="arg_type_2"
                            )
                        ],
                    ),
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="td_type_1"
                            )
                        ],
                        empty=False,
                        name="_ModelDictBase",
                        parent_class="typing.TypedDict",
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_2", type="td_type_2"
                            )
                        ],
                        empty=False,
                        name="ModelDict",
                        parent_class="_ModelDictBase",
                    ),
                ),
            ),
            '''

class _ModelDictBase(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    column_1: td_type_1


class ModelDict(_ModelDictBase, total=False):
    """TypedDict for properties that are not required."""

    column_2: td_type_2


class Model(models.Model):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: model_type_1
    column_2: model_type_2

    def __init__(self, column_1: arg_type_1, column_2: arg_type_2 = None) -> None:
        """Construct."""
        kwargs = {"column_1": column_1}
        if column_2 is not None:
            kwargs["column_2"] = column_2

        return super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, column_1: arg_type_1, column_2: arg_type_2 = None) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"column_1": column_1}
        if column_2 is not None:
            kwargs["column_2"] = column_2

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
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

    print(repr(source))
    print(repr(expected_source))

    assert source == expected_source
