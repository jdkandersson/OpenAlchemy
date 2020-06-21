"""Tests for type_."""
# pylint: disable=protected-access,unused-import

import datetime
import typing  # noqa: F401

import pytest
import sqlalchemy
import typeguard
from sqlalchemy.ext import declarative

import open_alchemy
from open_alchemy import exceptions
from open_alchemy import models_file

_ColSchemaArt = models_file.types.ColumnSchemaArtifacts


@pytest.mark.parametrize(
    "nullable, required, default, expected_type",
    [
        (False, True, None, "int"),
        (False, False, None, "typing.Optional[int]"),
        (True, True, None, "typing.Optional[int]"),
        (True, False, None, "typing.Optional[int]"),
        (False, False, 1, "int"),
        (True, False, 1, "int"),
    ],
    ids=[
        "not nullable required",
        "not nullable not required",
        "nullable required",
        "nullable not required",
        "not nullable default",
        "nullable default",
    ],
)
@pytest.mark.models_file
def test_arg_init(nullable, required, default, expected_type):
    """
    GIVEN nullable and required
    WHEN arg_init is called with the nullable and required
    THEN the expected type is returned.
    """
    artifacts = _ColSchemaArt(
        type="integer", nullable=nullable, required=required, default=default
    )

    returned_type = models_file._model._type.arg_init(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", "int"),
        ("object", '"RefModelDict"'),
        ("array", 'typing.Sequence["RefModelDict"]'),
    ],
    ids=["plain", "object", "array"],
)
@pytest.mark.models_file
def test_arg_from_dict(type_, expected_type):
    """
    GIVEN None format and required, False nullable and de_ref and given type
    WHEN arg_from_dict is called with the type, format, nullable, required and de_ref
    THEN the given expected type is returned.
    """
    artifacts = _ColSchemaArt(
        type=type_, nullable=False, required=True, de_ref="RefModel"
    )

    returned_type = models_file._model._type.arg_from_dict(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.models_file
def test_arg_from_dict_de_ref_none():
    """
    GIVEN object artifacts where de_ref is None
    WHEN arg_from_dict is called with the artifacts
    THEN MissingArgumentError is raised.
    """
    artifacts = _ColSchemaArt(type="object", de_ref=None)

    with pytest.raises(exceptions.MissingArgumentError):
        models_file._model._type.arg_from_dict(artifacts=artifacts)
