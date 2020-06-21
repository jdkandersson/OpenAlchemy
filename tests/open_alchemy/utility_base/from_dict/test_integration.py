"""Integration tests for dictionary to model conversion."""

import copy
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
    "schema, value",
    [
        pytest.param({"type": "string"}, "value 1", id="simple"),
        pytest.param(
            {"type": "string", "readOnly": False}, "value 1", id="readOnly False"
        ),
        pytest.param(
            {"type": "string", "readOnly": None}, "value 1", id="readOnly None"
        ),
        pytest.param({"type": "integer", "x-json": True}, 1, id="JSON integer"),
        pytest.param({"type": "number", "x-json": True}, 1.1, id="JSON number"),
        pytest.param({"type": "string", "x-json": True}, "value 1", id="JSON string"),
        pytest.param({"type": "boolean", "x-json": True}, True, id="JSON boolean"),
        pytest.param(
            {"type": "object", "x-json": True}, {"key": "value"}, id="JSON object"
        ),
        pytest.param({"type": "array", "x-json": True}, [1], id="JSON array"),
    ],
)
@pytest.mark.utility_base
def test_convert_valid(schema, value):
    """
    GIVEN valid schema for simple property and value
    WHEN convert is called with the schema and value
    THEN the converted value is returned.
    """
    returned_value = utility_base.from_dict.convert(
        schema=schema, value=copy.deepcopy(value)
    )

    assert returned_value == value


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
