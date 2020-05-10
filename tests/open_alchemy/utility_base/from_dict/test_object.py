"""Tests for object conversion."""

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, value, exception",
    [
        ({}, {}, exceptions.MalformedSchemaError),
        ({"x-de-$ref": "RefModel"}, 1, exceptions.InvalidInstanceError),
    ],
    ids=["no de-$-ref", "value not dict"],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, value, exception):
    """
    GIVEN invalid schema and value and expected exception
    WHEN convert is called with the schema and value
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.from_dict.object_.convert(value, schema=schema)


@pytest.mark.utility_base
def test_convert_invalid_missing_model(mocked_facades_models):
    """
    GIVEN mocked models facade that returns None for the model
    WHEN convert is called
    THEN SchemaNotFoundError is raised.
    """
    mocked_facades_models.get_model.return_value = None
    schema = {"x-de-$ref": "RefModel"}
    value = {}

    with pytest.raises(exceptions.SchemaNotFoundError):
        utility_base.from_dict.object_.convert(value, schema=schema)


@pytest.mark.utility_base
def test_convert_valid(mocked_facades_models):
    """
    GIVEN mocked models facade, schema and value
    WHEN convert is called
    THEN the referenced model is returned and constructed using from_dict with the
        value.
    """
    schema = {"x-de-$ref": "RefModel"}
    value = {"key": "value"}

    returned_value = utility_base.from_dict.object_.convert(value, schema=schema)

    mocked_facades_models.get_model.assert_called_once_with(name="RefModel")
    mocked_facades_models.get_model.return_value.from_dict.assert_called_once_with(
        **{"key": "value"}
    )
    expected_value = mocked_facades_models.get_model.return_value.from_dict.return_value
    assert returned_value == expected_value
