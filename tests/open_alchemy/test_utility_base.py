"""Tests for UtilityBase."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.utility_base
def test_to_dict_no_schema():
    """
    GIVEN class that derives from UtilityBase but does not define _schema
    WHEN to_dict is called
    THEN ModelAttributeError is raised.
    """
    model = type("model", (utility_base.UtilityBase,), {})
    instance = model()

    with pytest.raises(exceptions.ModelAttributeError):
        instance.to_dict()


@pytest.mark.utility_base
def test_to_dict_no_properties():
    """
    GIVEN class that derives from UtilityBase with a schema without properties
    WHEN to_dict is called
    THEN MalformedSchemaError is raised.
    """
    model = type("model", (utility_base.UtilityBase,), {"_schema": {}})
    instance = model()

    with pytest.raises(exceptions.MalformedSchemaError):
        instance.to_dict()


@pytest.mark.utility_base
def test_to_dict_no_type():
    """
    GIVEN class that derives from UtilityBase with a schema with a property without a
        type
    WHEN to_dict is called
    THEN MalformedSchemaError is raised.
    """
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": {"properties": {"key": {}}}}
    )
    instance = model()

    with pytest.raises(exceptions.TypeMissingError):
        instance.to_dict()


@pytest.mark.parametrize(
    "model_dict, expected_dict",
    [
        ({"_schema": {"properties": {}}}, {}),
        ({"_schema": {"properties": {}}, "key_1": "value 1"}, {}),
        ({"_schema": {"properties": {"key_1": {"type": "type 1"}}}}, {"key_1": None}),
        (
            {
                "_schema": {"properties": {"key_1": {"type": "type 1"}}},
                "key_1": "value 1",
            },
            {"key_1": "value 1"},
        ),
        (
            {
                "_schema": {
                    "properties": {
                        "key_1": {"type": "type 1"},
                        "key_2": {"type": "type 2"},
                    }
                },
                "key_1": "value 1",
                "key_2": "value 2",
            },
            {"key_1": "value 1", "key_2": "value 2"},
        ),
    ],
    ids=[
        "empty",
        "single not in schema",
        "single property missing",
        "single in schema",
        "multiple",
    ],
)
@pytest.mark.utility_base
def test_simple_type(model_dict, expected_dict):
    """
    GIVEN class that derives from UtilityBase with a given schema with properties that
        are not objects and expected object
    WHEN to_dict is called
    THEN the expected object is returned.
    """
    model = type("model", (utility_base.UtilityBase,), model_dict)
    instance = model()

    returned_dict = instance.to_dict()

    assert returned_dict == expected_dict


@pytest.mark.utility_base
def test_object_undefined():
    """
    GIVEN class that derives from UtilityBase with a schema with an object property
        that is not defined
    WHEN to_dict is called
    THEN None is returned for the property.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}},
    )
    instance = model()

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": None}


@pytest.mark.utility_base
def test_object_none():
    """
    GIVEN class that derives from UtilityBase with a schema with an object property
        that has a value of None
    WHEN to_dict is called
    THEN None is returned for the property.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}, "key": None},
    )
    instance = model()

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": None}


@pytest.mark.utility_base
def test_object_no_to_dict():
    """
    GIVEN class that derives from UtilityBase with a schema with an object property
        that does not have a to_dict function
    WHEN to_dict is called
    THEN InvalidModelInstanceError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}, "key": "value"},
    )
    instance = model()

    with pytest.raises(exceptions.InvalidModelInstanceError):
        instance.to_dict()


@pytest.mark.utility_base
def test_object():
    """
    GIVEN class that derives from UtilityBase with a schema with an object property
        that has a mock model
    WHEN to_dict is called
    THEN the mock object to_dict return value is returned as the property value.
    """
    mock_model = mock.MagicMock()
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}, "key": mock_model},
    )
    instance = model()

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": mock_model.to_dict.return_value}


def __init__(self, **kwargs):
    """COnstruct."""
    for name, value in kwargs.items():
        setattr(self, name, value)


@pytest.mark.utility_base
def test_malformed_dictionary():
    """
    GIVEN class that derives from UtilityBase and schema
    WHEN from_dict is called with a dictionary that does not satisfy the schema
    THEN MalformedModelDictionaryError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "integer"}},
                "required": ["key"],
            },
            "__init__": __init__,
        },
    )

    with pytest.raises(exceptions.MalformedModelDictionaryError):
        model.from_dict(**{})
