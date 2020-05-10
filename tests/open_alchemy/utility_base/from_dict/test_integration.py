"""Integration tests for dictionary to model conversion."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, exception",
    [
        ({}, exceptions.TypeMissingError),
        (
            {"type": "string", "readOnly": True},
            exceptions.MalformedModelDictionaryError,
        ),
        ({"type": "unsupported"}, exceptions.FeatureNotImplementedError),
    ],
    ids=["no type", "readOny", "unsupported"],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, exception):
    """
    GIVEN invalid schema and expected exception
    WHEN convert is called with the schema
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.from_dict.convert(schema=schema, value=mock.MagicMock())


@pytest.mark.parametrize(
    "schema",
    [
        ({"type": "string"}),
        ({"type": "string", "readOnly": False}),
        ({"type": "string", "readOnly": None}),
    ],
    ids=["simple", "readOnly False", "readOnly None"],
)
@pytest.mark.utility_base
def test_convert_valid(schema):
    """
    GIVEN valid schema for simple property and value
    WHEN convert is called with the schema and value
    THEN the converted value is returned.
    """
    value = "value 1"

    returned_value = utility_base.from_dict.convert(schema=schema, value=value)

    assert returned_value == "value 1"


@pytest.mark.utility_base
def test_convert_object(mocked_facades_models):
    """
    GIVEN schema for object property and value
    WHEN convert is called with the schema and value
    THEN the converted object is returned.
    """
    schema = {"type": "object", "x-de-$ref": "RefModel"}
    value = {"key": "value"}

    returned_value = utility_base.from_dict.convert(schema=schema, value=value)

    expected_value = mocked_facades_models.get_model.return_value.from_dict.return_value
    assert returned_value == expected_value


@pytest.mark.utility_base
def test_convert_array(mocked_facades_models):
    """
    GIVEN schema for array property and value
    WHEN convert is called with the schema and value
    THEN the converted array is returned.
    """
    schema = {"type": "array", "items": {"type": "object", "x-de-$ref": "RefModel"}}
    value = [{"key": "value"}]

    returned_value = utility_base.from_dict.convert(schema=schema, value=value)

    expected_value = [
        mocked_facades_models.get_model.return_value.from_dict.return_value
    ]
    assert returned_value == expected_value
