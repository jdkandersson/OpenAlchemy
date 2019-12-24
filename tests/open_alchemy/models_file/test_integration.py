"""Tests for models file."""

import pytest

from open_alchemy import models_file

DOCSTRING = '"""SQLAlchemy models based on models constructed by OpenAlchemy."""'
LONG_NAME = "extremely_long_name_that_will_cause_wrapping_aaaaaaaaaaaaaaaaaa"


@pytest.mark.parametrize(
    "schemas, expected_source",
    [
        (
            [({"properties": {"id": {"type": "integer"}}}, "Model")],
            f'''{DOCSTRING}
# pylint: disable=no-member

import typing

from open_alchemy import models


class Model(models.Model):
    """Model SQLAlchemy model."""

    id: typing.Optional[int]
''',
        ),
        (
            [
                ({"properties": {"id": {"type": "integer"}}}, "Model1"),
                ({"properties": {"id": {"type": "string"}}}, "Model2"),
            ],
            f'''{DOCSTRING}
# pylint: disable=no-member

import typing

from open_alchemy import models


class Model1(models.Model1):
    """Model1 SQLAlchemy model."""

    id: typing.Optional[int]


class Model2(models.Model2):
    """Model2 SQLAlchemy model."""

    id: typing.Optional[str]
''',
        ),
        (
            [({"properties": {LONG_NAME: {"type": "integer"}}}, "Model")],
            f'''{DOCSTRING}
# pylint: disable=no-member

import typing

from open_alchemy import models


class Model(models.Model):
    """Model SQLAlchemy model."""

    extremely_long_name_that_will_cause_wrapping_aaaaaaaaaaaaaaaaaa: typing.Optional[
        int
    ]
''',
        ),
    ],
    ids=["single", "multiple", "black formatting"],
)
@pytest.mark.models_file
def test_integration(schemas, expected_source):
    """
    GIVEN schema and name
    WHEN schema is added to the models file and the models file is generated
    THEN the models source code is returned.
    """
    models = models_file.ModelsFile()
    for schema, name in schemas:
        models.add_model(schema=schema, name=name)
    source = models.generate_models()

    assert source == expected_source
