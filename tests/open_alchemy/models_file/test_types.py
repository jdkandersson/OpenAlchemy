"""Tests for types."""

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "description, columns, expected_docstring",
    [
        (None, [], "SQLAlchemy model protocol."),
        (
            "description 1",
            [],
            """
    SQLAlchemy model protocol.

    description 1

    """,
        ),
        (
            "description 1 that is very long and will cause line wrapping if its "
            "longggg",
            [],
            """
    SQLAlchemy model protocol.

    description 1 that is very long and will cause line wrapping if its longggg

    """,
        ),
        (
            "description 1 that is very long and will cause line wrapping if its "
            "longggg enough and I can keep on thinking of more words to put here to "
            "ensureeeeeee that",
            [],
            """
    SQLAlchemy model protocol.

    description 1 that is very long and will cause line wrapping if its longggg
    enough and I can keep on thinking of more words to put here to ensureeeeeee
    that

    """,
        ),
        (
            "description 1 that is very long and will cause line wrapping if its "
            "longgggg",
            [],
            """
    SQLAlchemy model protocol.

    description 1 that is very long and will cause line wrapping if its
    longgggg

    """,
        ),
        (
            None,
            [models_file.types.ColumnArtifacts(name="column_1", type="type_1")],
            """
    SQLAlchemy model protocol.

    Attrs:
        column_1: The column_1 of the Model 1.

    """,
        ),
        (
            None,
            [
                models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
            ],
            """
    SQLAlchemy model protocol.

    Attrs:
        column_1: The column_1 of the Model 1.
        column_2: The column_2 of the Model 1.

    """,
        ),
        (
            "description 1",
            [models_file.types.ColumnArtifacts(name="column_1", type="type_1")],
            """
    SQLAlchemy model protocol.

    description 1

    Attrs:
        column_1: The column_1 of the Model 1.

    """,
        ),
    ],
    ids=[
        "description None             columns empty",
        "description short            columns empty",
        "description long no wrap     columns empty",
        "description long wrap single columns empty",
        "description long wrap mult   columns empty",
        "description None             single column",
        "description None             multiple columns",
        "description short            single column",
    ],
)
@pytest.mark.models_file
def test_docstring(description, columns, expected_docstring):
    """
    GIVEN description and columns
    WHEN model_docstring is called with the artifacts with the description and columns
    THEN the expected docstring is returned.
    """
    artifacts = models_file.types.SQLAlchemyModelArtifacts(
        name="Model 1",
        empty=not columns,
        columns=columns,
        arg=models_file.types.ArgArtifacts(required=[], not_required=[]),
        parent_cls="Parent 1",
        description=description,
    )

    returned_description = models_file.types.model_docstring(artifacts=artifacts)

    assert returned_description == expected_docstring


@pytest.mark.parametrize(
    "columns, return_value_description, expected_docstring",
    [
        ([], None, "function description 1"),
        (
            [],
            "return value description 1",
            """
        function description 1

        Returns:
            return value description 1

        """,
        ),
        (
            [models_file.types.ColumnArtifacts(name="column_1", type="type_1")],
            None,
            """
        function description 1

        Args:
            column_1: The column_1 of the Model 1.

        """,
        ),
        (
            [models_file.types.ColumnArtifacts(name="column_1", type="type_1")],
            "return value description 1",
            """
        function description 1

        Args:
            column_1: The column_1 of the Model 1.

        Returns:
            return value description 1

        """,
        ),
        (
            [
                models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
            ],
            None,
            """
        function description 1

        Args:
            column_1: The column_1 of the Model 1.
            column_2: The column_2 of the Model 1.

        """,
        ),
    ],
    ids=[
        "columns empty    rv description None",
        "columns empty    rv defined",
        "single column    rv description None",
        "single column    rv description defined",
        "multiple columns rv description None",
    ],
)
@pytest.mark.models_file
def test_model_function_docstring(
    columns, return_value_description, expected_docstring
):
    """
    GIVEN columns
    WHEN model_function_docstring is called with the artifacts with the columns
    THEN the expected docstring is returned.
    """
    artifacts = models_file.types.SQLAlchemyModelArtifacts(
        name="Model 1",
        empty=not columns,
        columns=columns,
        arg=models_file.types.ArgArtifacts(required=[], not_required=[]),
        parent_cls="Parent 1",
        description=None,
    )

    returned_description = models_file.types.model_function_docstring(
        artifacts=artifacts,
        function_description="function description 1",
        return_value_description=return_value_description,
    )

    assert returned_description == expected_docstring


@pytest.mark.parametrize(
    "artifacts, expected_docs",
    [
        (
            models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
            "column_1: The column_1 of the Model.",
        ),
        (
            models_file.types.ColumnArtifacts(
                name="column_1", type="type_1", description="description 1"
            ),
            "column_1: description 1",
        ),
        (
            models_file.types.ColumnArtifacts(
                name="column_1",
                type="type_1",
                description=(
                    "description 1 that is very long and will cause line wrappingg"
                ),
            ),
            "column_1: description 1 that is very long and will cause line wrappingg",
        ),
        (
            models_file.types.ColumnArtifacts(
                name="column_1",
                type="type_1",
                description=(
                    "description 1 that is very long and will cause line wrappinggg"
                ),
            ),
            """column_1: description 1 that is very long and will cause line
            wrappinggg""",
        ),
        (
            models_file.types.ColumnArtifacts(
                name="column_1",
                type="type_1",
                description=(
                    "description 1 that is very long and will cause line wrappingg if "
                    "its long enough and I can keep on thinking of more words toooooo "
                    "write"
                ),
            ),
            """column_1: description 1 that is very long and will cause line wrappingg
            if its long enough and I can keep on thinking of more words toooooo
            write""",
        ),
        (
            models_file.types.ColumnArtifacts(
                name="column_1",
                type="type_1",
                description=(
                    "description 1 that is very long and will cause line wrappingg if "
                    "its long enough and I can keep on thinking of more words toooooo "
                    "write ensure that even more lines will get wrapped to the next "
                    "line hmm"
                ),
            ),
            """column_1: description 1 that is very long and will cause line wrappingg
            if its long enough and I can keep on thinking of more words toooooo
            write ensure that even more lines will get wrapped to the next line
            hmm""",
        ),
    ],
    ids=[
        "no description",
        "short description",
        "long description no wrap",
        "long description wrap single",
        "long description wrap multiple",
        "long description wrap even more",
    ],
)
@pytest.mark.models_file
def test_attr(artifacts, expected_docs):
    """
    GIVEN artifacts and name of a model
    WHEN model_attr_docs is called with the artifacts and name
    THEN the expected docs are returned.
    """
    returned_docs = models_file.types.model_attr_docs(
        artifacts=artifacts, model_name="Model"
    )

    assert returned_docs == expected_docs


@pytest.mark.parametrize(
    "description, expected_docs",
    [
        (
            "description 1 that is very long and will cause lineeeeeee",
            "column_1: description 1 that is very long and will cause lineeeeeee",
        ),
        (
            "description 1 that is very long and will cause lineeeeeeee",
            """column_1: description 1 that is very long and will cause
                lineeeeeeee""",
        ),
        (
            "description 1 that is very long and will cause lineeeeeeee wrapping if "
            "its long enough and I can keep onnnnnnn thinking",
            """column_1: description 1 that is very long and will cause
                lineeeeeeee wrapping if its long enough and I can keep onnnnnnn
                thinking""",
        ),
        (
            "description 1 that is very long and will cause lineeeeeeee wrapping if "
            "its long enough and I can keep onnnnnnn thinking of more words to write "
            "ensure that even more linesssss will",
            """column_1: description 1 that is very long and will cause
                lineeeeeeee wrapping if its long enough and I can keep onnnnnnn
                thinking of more words to write ensure that even more linesssss
                will""",
        ),
    ],
    ids=[
        "long description no wrap",
        "long description wrap single",
        "long description wrap multiple",
        "long description wrap even more",
    ],
)
@pytest.mark.models_file
def test_arg(description, expected_docs):
    """
    GIVEN artifacts and name of a model
    WHEN model_arg_docs is called with the artifacts and name
    THEN the expected docs are returned.
    """
    artifacts = models_file.types.ColumnArtifacts(
        name="column_1", type="type_1", description=description
    )

    returned_docs = models_file.types.model_arg_docs(
        artifacts=artifacts, model_name="Model"
    )

    assert returned_docs == expected_docs


@pytest.mark.models_file
def test_sqlalchemy_model_artifacts_docs():
    """
    GIVEN artifacts
    WHEN documentation properties are accessed
    THEN the documentation is produced.
    """
    artifacts = models_file.types.SQLAlchemyModelArtifacts(
        name="Model 1",
        empty=False,
        columns=[models_file.types.ColumnArtifacts(name="column_1", type="type_1")],
        arg=models_file.types.ArgArtifacts(required=[], not_required=[]),
        parent_cls="Parent 1",
        description="description 1",
    )

    assert (
        artifacts.docstring
        == """
    SQLAlchemy model protocol.

    description 1

    Attrs:
        column_1: The column_1 of the Model 1.

    """
    )
    assert (
        artifacts.init_docstring
        == """
        Construct.

        Args:
            column_1: The column_1 of the Model 1.

        """
    )
    assert (
        artifacts.from_dict_docstring
        == """
        Construct from a dictionary (eg. a POST payload).

        Args:
            column_1: The column_1 of the Model 1.

        Returns:
            Model instance based on the dictionary.

        """
    )
