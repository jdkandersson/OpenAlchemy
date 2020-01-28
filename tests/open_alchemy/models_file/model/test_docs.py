"""Tests for creating documentation for a model."""

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "description, expected_docstring",
    [
        (None, "SQLAlchemy model protocol."),
        (
            "description 1",
            """
    SQLAlchemy model protocol.

    description 1
    """,
        ),
        (
            "description 1 that is very long and will cause line wrapping if its long "
            "enough",
            """
    SQLAlchemy model protocol.

    description 1 that is very long and will cause line wrapping if its long
    enough
    """,
        ),
    ],
    ids=["None", "short", "long"],
)
@pytest.mark.models_file
def test_docstring(description, expected_docstring):
    """
    GIVEN description
    WHEN docstring is called with the description
    THEN the expected description is returned.
    """
    returned_description = models_file.docs.docstring(description=description)

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
                    "description 1 that is very long and will cause line wrapping if"
                ),
            ),
            """column_1: description 1 that is very long and will cause line wrapping
            if""",
        ),
    ],
    ids=["no description", "short description", "long description"],
)
@pytest.mark.models_file
def test_attr(artifacts, expected_docs):
    """
    GIVEN artifacts and name of a model
    WHEN attr is called with the artifacts and name
    THEN the expected docs are returned.
    """
    returned_docs = models_file.docs.attr(artifacts=artifacts, model_name="Model")

    assert returned_docs == expected_docs
