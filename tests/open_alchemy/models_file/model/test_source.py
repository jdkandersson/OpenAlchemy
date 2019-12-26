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
        (
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model", columns=[], empty=True
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

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
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
                            name="column_1", type="type_1"
                        )
                    ],
                    empty=False,
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[], empty=True, name=None, parent_class=None
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="type_1"
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

    column_1: type_1


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
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        )
                    ],
                    empty=False,
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="type_1"
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

    column_1: type_1


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
            models_file.types.ModelArtifacts(
                sqlalchemy=models_file.types.SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[
                        models_file.types.ColumnArtifacts(
                            name="column_1", type="type_1"
                        ),
                        models_file.types.ColumnArtifacts(
                            name="column_2", type="type_2"
                        ),
                    ],
                    empty=False,
                ),
                typed_dict=models_file.types.TypedDictArtifacts(
                    required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_1", type="type_1"
                            )
                        ],
                        empty=False,
                        name="_ModelDictBase",
                        parent_class="typing.TypedDict",
                    ),
                    not_required=models_file.types.TypedDictClassArtifacts(
                        props=[
                            models_file.types.ColumnArtifacts(
                                name="column_2", type="type_2"
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

    column_1: type_1


class ModelDict(_ModelDictBase, total=False):
    """TypedDict for properties that are not required."""

    column_2: type_2


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
