"""Tests for converting array values to columns."""

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.parametrize(
    "schema, value, exception",
    [
        ({}, [], exceptions.MalformedSchemaError),
        ({"items": {}}, [], exceptions.TypeMissingError),
        ({"items": {"type": "string"}}, [], exceptions.MalformedSchemaError),
        (
            {"items": {"type": "object", "x-de-$ref": "RefSchema"}},
            1,
            exceptions.InvalidInstanceError,
        ),
    ],
    ids=[
        "items missing in schema",
        "type missing in items schema",
        "items not object in schema",
        "value not array",
    ],
)
@pytest.mark.utility_base
def test_convert_invalid(schema, value, exception):
    """
    GIVEN invalid schema and value and expected exception
    WHEN convert is called with the schema and value
    THEN the expected exception is raised.
    """
    with pytest.raises(exception):
        utility_base.from_dict.array.convert(value, schema=schema)


@pytest.mark.parametrize(
    "value, from_dict_side_effect, expected_value",
    [
        (None, None, None),
        ([], None, []),
        ([{"key": "value"}], [{"key": "value"}], [{"key": "value"}]),
        (
            [{"key_1": "value 1"}, {"key_2": "value 2"}],
            [{"key_1": "value 1"}, {"key_2": "value 2"}],
            [{"key_1": "value 1"}, {"key_2": "value 2"}],
        ),
    ],
    ids=["None", "empty", "single", "multiple"],
)
@pytest.mark.utility_base
def test_convert_valid(
    value, from_dict_side_effect, expected_value, mocked_facades_models
):
    """
    GIVEN invalid schema and value and expected exception
    WHEN convert is called with the schema and value
    THEN the expected exception is raised.
    """
    schema = {"items": {"type": "object", "x-de-$ref": "RefModel"}}
    from_dict_func = mocked_facades_models.get_model.return_value.from_dict
    from_dict_func.side_effect = from_dict_side_effect

    returned_value = utility_base.from_dict.array.convert(value, schema=schema)

    assert returned_value == expected_value
