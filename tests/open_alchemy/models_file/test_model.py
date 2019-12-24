"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.ModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
            ),
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    column_1: type_1''',
        ),
        (
            models_file.types.ModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
            ),
            '''

class Model(open_alchemy.Model):
    """Model SQLAlchemy model."""

    column_1: type_1
    column_2: type_2''',
        ),
    ],
    ids=["single column", "multiple column"],
)
@pytest.mark.models_file
def test_generate(artifacts, expected_source):
    """
    GIVEN model artifacts
    WHEN generate is called with the artifacts
    THEN the source code for the model class is returned.
    """
    source = models_file._model.generate(artifacts=artifacts)

    assert source == expected_source
