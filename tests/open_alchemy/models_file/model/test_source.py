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
            _SQLAlchemyModelArtifacts(
                name="Model",
                columns=[],
                empty=True,
                arg=_ArgArtifacts(required=[], not_required=[]),
            ),
            '''

class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    def __init__(self) -> None:
        """Construct."""
        kwargs = {}

        super().__init__(**kwargs)

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
            ),
            '''

class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: type_1

    def __init__(self, column_1: init_type_1) -> None:
        """Construct."""
        kwargs = {"column_1": column_1}

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, column_1: fd_type_1) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"column_1": column_1}

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
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
            ),
            '''

class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    column_1: type_1
    column_2: type_2

    def __init__(self, column_1: init_type_1, column_2: init_type_2) -> None:
        """Construct."""
        kwargs = {"column_1": column_1, "column_2": column_2}

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, column_1: fd_type_1, column_2: fd_type_2) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"column_1": column_1, "column_2": column_2}

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
            _TypedDictArtifacts(
                required=_TypedDictClassArtifacts(
                    props=[_ColumnArtifacts(name="column_1", type="type_1")],
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
            _TypedDictArtifacts(
                required=_TypedDictClassArtifacts(
                    props=[
                        _ColumnArtifacts(name="column_1", type="type_1"),
                        _ColumnArtifacts(name="column_2", type="type_2"),
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
            _TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=_TypedDictClassArtifacts(
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
            _TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=_TypedDictClassArtifacts(
                    props=[_ColumnArtifacts(name="column_1", type="type_1")],
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
            _TypedDictArtifacts(
                required=None,  # type: ignore
                not_required=_TypedDictClassArtifacts(
                    props=[
                        _ColumnArtifacts(name="column_1", type="type_1"),
                        _ColumnArtifacts(name="column_2", type="type_2"),
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
        (_ArgArtifacts(required=[], not_required=[]), ""),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[],
            ),
            ", column_1: init_type_1",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
            ),
            ", column_1: init_type_1 = None",
        ),
        (
            _ArgArtifacts(
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
            ", column_1: init_type_1, column_2: init_type_2",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    )
                ],
            ),
            ", column_1: init_type_1, column_2: init_type_2 = None",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
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
            ),
            ", column_1: init_type_1 = None, column_2: init_type_2 = None",
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
def test_arg_input_init(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_input_init is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_input_init(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (_ArgArtifacts(required=[], not_required=[]), ""),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[],
            ),
            ", column_1: fd_type_1",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
            ),
            ", column_1: fd_type_1 = None",
        ),
        (
            _ArgArtifacts(
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
            ", column_1: fd_type_1, column_2: fd_type_2",
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    )
                ],
            ),
            ", column_1: fd_type_1, column_2: fd_type_2 = None",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
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
            ),
            ", column_1: fd_type_1 = None, column_2: fd_type_2 = None",
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
def test_arg_input_from_dict(artifacts, expected_source):
    """
    GIVEN artifacts
    WHEN arg_input_from_dict is called with the artifacts
    THEN the expected source is returned.
    """
    source = models_file._model._source.arg_input_from_dict(artifacts=artifacts)

    assert source == expected_source


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (_ArgArtifacts(required=[], not_required=[]), "kwargs = {}"),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[],
            ),
            'kwargs = {"column_1": column_1}',
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
            ),
            """kwargs = {}
        if column_1 is not None:
            kwargs["column_1"] = column_1""",
        ),
        (
            _ArgArtifacts(
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
            'kwargs = {"column_1": column_1, "column_2": column_2}',
        ),
        (
            _ArgArtifacts(
                required=[
                    _ColumnArgArtifacts(
                        name="column_1",
                        init_type="init_type_1",
                        from_dict_type="fd_type_1",
                    )
                ],
                not_required=[
                    _ColumnArgArtifacts(
                        name="column_2",
                        init_type="init_type_2",
                        from_dict_type="fd_type_2",
                    )
                ],
            ),
            """kwargs = {"column_1": column_1}
        if column_2 is not None:
            kwargs["column_2"] = column_2""",
        ),
        (
            _ArgArtifacts(
                required=[],
                not_required=[
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
            _ModelArtifacts(
                sqlalchemy=_SQLAlchemyModelArtifacts(
                    name="Model",
                    columns=[],
                    empty=True,
                    arg=_ArgArtifacts(required=[], not_required=[]),
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


class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    def __init__(self) -> None:
        """Construct."""
        kwargs = {}

        super().__init__(**kwargs)

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


class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: model_type_1

    def __init__(self, col_1: arg_i_type_1 = None) -> None:
        """Construct."""
        kwargs = {}
        if col_1 is not None:
            kwargs["col_1"] = col_1

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1 = None) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {}
        if col_1 is not None:
            kwargs["col_1"] = col_1

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
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


class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: model_type_1

    def __init__(self, col_1: arg_i_type_1) -> None:
        """Construct."""
        kwargs = {"col_1": col_1}

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"col_1": col_1}

        return super().from_dict(**kwargs)

    def to_dict(self) -> ModelDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()''',
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


class Model(models.Model):  # type: ignore
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    col_1: model_type_1
    col_2: model_type_2

    def __init__(self, col_1: arg_i_type_1, col_2: arg_i_type_2 = None) -> None:
        """Construct."""
        kwargs = {"col_1": col_1}
        if col_2 is not None:
            kwargs["col_2"] = col_2

        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, col_1: arg_fd_type_1, col_2: arg_fd_type_2 = None) -> "Model":
        """Construct from a dictionary (eg. a POST payload)."""
        kwargs = {"col_1": col_1}
        if col_2 is not None:
            kwargs["col_2"] = col_2

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
