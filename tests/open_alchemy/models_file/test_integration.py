"""Tests for models file."""

import pytest

from open_alchemy import models_file

DOCSTRING = '"""SQLAlchemy models based on models constructed by OpenAlchemy."""'


@pytest.mark.models_file
def test_integration():
    """
    GIVEN schema and name
    WHEN schema is added to the models file and the models file is generated
    THEN the models source code is returned.
    """
    schema_1 = {"properties": {"id": {"type": "integer"}}}
    schema_2 = {"properties": {"id": {"type": "string"}}}

    models = models_file.ModelsFile()
    models.add_model(schema=schema_1, name="Model1")
    models.add_model(schema=schema_2, name="Model2")
    source = models.generate_models()

    expected_source = f'''{DOCSTRING}
# pylint: disable=no-member

import typing

from open_alchemy import models


class Model1(models.Model1):
    """Model1 SQLAlchemy model."""

    id: typing.Optional[int]


class Model2(models.Model2):
    """Model2 SQLAlchemy model."""

    id: typing.Optional[str]
'''

    assert source == expected_source
