"""Tests for model."""

import pytest

from open_alchemy.models_file import types
from open_alchemy.models_file.model import source as model_source

_ColumnArtifacts = types.ColumnArtifacts
_TypedDictArtifacts = types.TypedDictArtifacts
_TypedDictClassArtifacts = types.TypedDictClassArtifacts


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
    source = model_source.typed_dict_required(artifacts=artifacts)

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
    source = model_source.typed_dict_not_required(artifacts=artifacts)

    assert source == expected_source
