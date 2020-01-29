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
    WHEN model_docstring is called with the description
    THEN the expected description is returned.
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
@pytest.mark.only_this
def test_attr(artifacts, expected_docs):
    """
    GIVEN artifacts and name of a model
    WHEN model_attr_docs is called with the artifacts and name
    THEN the expected docs are returned.
    """
    returned_docs = models_file.types.model_attr_docs(
        artifacts=artifacts, model_name="Model"
    )

    print(repr(returned_docs))
    print(repr(expected_docs))

    assert returned_docs == expected_docs


@pytest.mark.models_file
def test_sqlalchemy_model_artifacts_docstring():
    """
    GIVEN artifacts
    WHEN .docstring is access
    THEN a docstring is produced.
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
