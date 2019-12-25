"""Tests for model."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file


@pytest.mark.parametrize(
    "artifacts, expected_source",
    [
        (
            models_file.types.SQLAlchemyModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1")
                ],
            ),
            '''

class Model(models.Model):
    """Model SQLAlchemy model."""

    column_1: type_1''',
        ),
        (
            models_file.types.SQLAlchemyModelArtifacts(
                name="Model",
                columns=[
                    models_file.types.ColumnArtifacts(name="column_1", type="type_1"),
                    models_file.types.ColumnArtifacts(name="column_2", type="type_2"),
                ],
            ),
            '''

class Model(models.Model):
    """Model SQLAlchemy model."""

    column_1: type_1
    column_2: type_2''',
        ),
    ],
    ids=["single column", "multiple column"],
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
                model_name="Model",
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
    """Model TypedDict for properties that are required."""

    column_1: type_1''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                model_name="Model",
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
    """Model TypedDict for properties that are required."""

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
                model_name="Model",
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
    """Model TypedDict for properties that are not required."""''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                model_name="Model",
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
    """Model TypedDict for properties that are not required."""

    column_1: type_1''',
        ),
        (
            models_file.types.TypedDictArtifacts(
                model_name="Model",
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
    """Model TypedDict for properties that are not required."""

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

    print(repr(source))
    print(repr(expected_source))

    assert source == expected_source
