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
    returned_description = models_file.docs.docstring(description)

    assert returned_description == expected_docstring
