"""Tests for SQLAlchemy JSON property facade."""

import functools

import pytest
import sqlalchemy

from open_alchemy import types
from open_alchemy.facades.sqlalchemy import json
from open_alchemy.schemas.artifacts import types as artifacts_types


def _create_artifacts():
    """Create column artifacts."""
    return artifacts_types.JsonPropertyArtifacts(
        type=types.PropertyType.JSON,
        open_api=artifacts_types.OpenApiJsonPropertyArtifacts(
            nullable=None,
            read_only=None,
            write_only=None,
        ),
        extension=artifacts_types.ExtensionJsonPropertyArtifacts(
            primary_key=None,
            index=None,
            unique=None,
            foreign_key=None,
            kwargs=None,
            foreign_key_kwargs=None,
        ),
        schema={"type": "integer"},
        required=False,
        description=None,
    )


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct():
    """
    GIVEN artifacts for a type
    WHEN construct is called with the artifacts
    THEN a column with the JSON type is returned.
    """
    artifacts = _create_artifacts()

    returned_column = json.construct(artifacts=artifacts)

    assert isinstance(returned_column, sqlalchemy.Column)
    assert isinstance(returned_column.type, sqlalchemy.JSON)


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_foreign_key():
    """
    GIVEN artifacts with foreign key
    WHEN construct is called with the artifacts
    THEN a column with a foreign key is returned.
    """
    artifacts = _create_artifacts()
    artifacts.extension.foreign_key = "table.column"

    returned_column = json.construct(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('table.column')"
    assert foreign_key.name is None


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_foreign_key_kwargs():
    """
    GIVEN artifacts with foreign key and foreign key kwargs
    WHEN construct is called with the artifacts
    THEN a column with a foreign key with the kwargs is returned.
    """
    artifacts = _create_artifacts()
    artifacts.extension.foreign_key = "table.column"
    artifacts.extension.foreign_key_kwargs = {"name": "name 1"}

    returned_column = json.construct(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert foreign_key.name == "name 1"


CONSTRUCT_ARGS_TESTS = [
    pytest.param("open_api", "nullable", True, "nullable", True, id="nullable true"),
    pytest.param("open_api", "nullable", False, "nullable", False, id="nullable false"),
    pytest.param(
        "extension", "primary_key", None, "primary_key", False, id="primary key None"
    ),
    pytest.param(
        "extension", "primary_key", False, "primary_key", False, id="primary key False"
    ),
    pytest.param(
        "extension", "primary_key", True, "primary_key", True, id="primary key True"
    ),
    pytest.param("extension", "index", None, "index", None, id="index None"),
    pytest.param("extension", "index", False, "index", False, id="index False"),
    pytest.param("extension", "index", True, "index", True, id="index True"),
    pytest.param("extension", "unique", None, "unique", None, id="unique None"),
    pytest.param("extension", "unique", False, "unique", False, id="unique False"),
    pytest.param("extension", "unique", True, "unique", True, id="unique True"),
]


@pytest.mark.parametrize(
    "art_parent_key, art_item_key, art_value, column_key, column_value",
    CONSTRUCT_ARGS_TESTS,
)
@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_args(
    art_parent_key, art_item_key, art_value, column_key, column_value
):
    """
    GIVEN artifacts where a key has been set to a value
    WHEN construct is called with the artifacts
    THEN a column where the key has the expected value is returned.
    """
    artifacts = _create_artifacts()
    setattr(getattr(artifacts, art_parent_key), art_item_key, art_value)

    returned_column = json.construct(artifacts=artifacts)

    assert (
        functools.reduce(getattr, column_key.split("."), returned_column)
        == column_value
    )


@pytest.mark.facade
@pytest.mark.sqlalchemy
def test_construct_kwargs():
    """
    GIVEN artifacts with kwargs
    WHEN construct is called with the artifacts
    THEN the column is constructed with the kwargs.
    """
    artifacts = _create_artifacts()
    artifacts.extension.kwargs = {"doc": "doc 1"}

    returned_column = json.construct(artifacts=artifacts)

    assert returned_column.doc == "doc 1"
