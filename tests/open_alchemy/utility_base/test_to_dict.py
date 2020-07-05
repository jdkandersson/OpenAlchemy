"""Tests for UtilityBase."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.utility_base
def test_to_dict_no_schema(__init__):
    """
    GIVEN class that derives from UtilityBase but does not define _schema
    WHEN to_dict is called
    THEN ModelAttributeError is raised.
    """
    model = type("model", (utility_base.UtilityBase,), {"__init__": __init__})
    instance = model()

    with pytest.raises(exceptions.ModelAttributeError):
        instance.to_dict()


@pytest.mark.utility_base
def test_to_dict_no_properties(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema without properties
    WHEN to_dict is called
    THEN MalformedSchemaError is raised.
    """
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": {}, "__init__": __init__}
    )
    instance = model()

    with pytest.raises(exceptions.MalformedSchemaError):
        instance.to_dict()


@pytest.mark.parametrize(
    "schema, value, expected_value",
    [
        pytest.param(
            {"properties": {"key": {"type": "integer"}}},
            {"key": 1},
            {"key": 1},
            id="single",
        ),
        pytest.param(
            {"properties": {"key": {"type": "integer"}}},
            {"key": None},
            {},
            id="single null value not return",
        ),
        pytest.param(
            {"properties": {"key": {"type": "integer", "nullable": True}}},
            {"key": None},
            {"key": None},
            id="single null value return",
        ),
        pytest.param(
            {"properties": {"key": {"type": "integer", "writeOnly": True}}},
            {"key": 1},
            {},
            id="single writeOnly",
        ),
        pytest.param(
            {"properties": {"key_1": {"type": "integer"}, "key_2": {"type": "string"}}},
            {"key_1": 1, "key_2": "value 2"},
            {"key_1": 1, "key_2": "value 2"},
            id="multiple",
        ),
    ],
)
@pytest.mark.utility_base
def test_valid(__init__, schema, value, expected_value):
    """
    GIVEN class that derives from UtilityBase with a schema and the expected value
    WHEN to_dict is called
    THEN the expected value is returned.
    """
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )
    instance = model(**value)

    returned_dict = instance.to_dict()

    assert returned_dict == expected_value


@pytest.mark.utility_base
def test_to_dict_backrefs_object(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an object backref
    WHEN to_dict is called
    THEN the backref value is not returned.
    """
    mock_model = mock.MagicMock()
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key_1": {"type": "integer"}},
                "x-backrefs": {"key_2": {"type": "object", "x-de-$ref": "RefModel"}},
            },
            "__init__": __init__,
        },
    )
    instance = model(**{"key_1": 1, "key_2": mock_model})

    returned_dict = instance.to_dict()

    assert returned_dict == {"key_1": 1}


@pytest.mark.utility_base
def test_to_dict_error(__init__):
    """
    GIVEN schema and value that raises an error
    WHEN model is defined with the schema and constructed with to_dict
    THEN raised error includes information about the model schema and property.
    """
    schema = {"properties": {"key_1": {"type": "object"}}}
    dictionary = {"key_1": 1}
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )
    instance = model(**dictionary)

    try:
        instance.to_dict()
    except exceptions.BaseError as exc:
        # pylint: disable=no-member
        assert exc.schema == {"properties": {"key_1": {"type": "object"}}}
        assert exc.property_schema == {"type": "object"}
        assert exc.property_name == "key_1"
        assert exc.property_value == 1
    else:
        raise AssertionError("Should have raised.")


@pytest.mark.utility_base
def test_to_dict_inheritance_call(mocked_facades_models, __init__):
    """
    GIVEN class that derives from UtilityBase with a schema that inherits
    WHEN to_dict is called
    THEN the dictionary based on the parent and child properties is returned.
    """
    schema = {
        "type": "object",
        "properties": {"key": {"type": "string"}},
        "x-inherits": "Parent",
    }
    mocked_facades_models.get_model.return_value.instance_to_dict.return_value = {
        "parent_key": "parent value"
    }
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )
    instance = model(**{"key": "value", "parent_key": "parent value"})

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": "value", "parent_key": "parent value"}
    mocked_facades_models.get_model.assert_called_once_with(name="Parent")
    check_func = mocked_facades_models.get_model.return_value.instance_to_dict
    check_func.assert_called_once_with(instance)


@pytest.mark.utility_base
def test_to_str(__init__):
    """
    GIVEN class that derives from UtilityBase with a given schema with properties
    WHEN to_str is called
    THEN the JSON representation of the properties is returned.
    """
    model = type(
        "Model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key_1": {"type": "integer"}}},
            "__init__": __init__,
        },
    )
    instance = model(key_1=1)

    returned_str = instance.to_str()

    assert returned_str == '{"key_1": 1}'
    assert str(instance) == '{"key_1": 1}'
    assert repr(instance) == "open_alchemy.models.Model(key_1=1)"
