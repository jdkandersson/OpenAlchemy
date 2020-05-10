"""Tests for UtilityBase."""

import datetime

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


@pytest.mark.utility_base
def test_from_dict_malformed_dictionary(__init__):
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


@pytest.mark.utility_base
def test_from_dict_argument_not_in_properties(__init__):
    """
    GIVEN dictionary with a key which is not a property in the schema
    WHEN from_dict is called with the dictionary
    THEN MalformedModelDictionaryError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {}}, "__init__": __init__},
    )

    with pytest.raises(exceptions.MalformedModelDictionaryError):
        model.from_dict(**{"key": "value"})


@pytest.mark.parametrize(
    "schema, dictionary",
    [
        ({"properties": {"key_1": {"type": "integer"}}}, {}),
        ({"properties": {"key_1": {"type": "integer"}}}, {"key_1": 1}),
        (
            {"properties": {"key_1": {"type": "integer"}}, "required": ["key_1"]},
            {"key_1": 1},
        ),
        (
            {
                "properties": {
                    "key_1": {"type": "integer"},
                    "key_2": {"type": "integer"},
                }
            },
            {"key_1": 11, "key_2": 12},
        ),
    ],
    ids=[
        "single not required not given",
        "single not required given",
        "single required given",
        "multiple",
    ],
)
@pytest.mark.utility_base
def test_from_dict(schema, dictionary, __init__):
    """
    GIVEN schema and dictionary to use for construction
    WHEN model is defined with the schema and constructed with from_dict
    THEN the instance has the properties from the dictionary.
    """
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )

    instance = model.from_dict(**dictionary)

    for key, value in dictionary.items():
        assert getattr(instance, key) == value


@pytest.mark.utility_base
def test_from_dict_error(__init__):
    """
    GIVEN schema and value that raises an error
    WHEN model is defined with the schema and constructed with from_dict
    THEN raised error includes information about the model schema and property.
    """
    schema = {"properties": {"key_1": {"type": "object"}}}
    dictionary = {"key_1": {}}
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )

    try:
        model.from_dict(**dictionary)
    except exceptions.BaseError as exc:
        # pylint: disable=no-member
        assert exc.schema == {"properties": {"key_1": {"type": "object"}}}
        assert exc.property_schema == {"type": "object"}
        assert exc.property_name == "key_1"
        assert exc.property_value == {}
    else:
        raise AssertionError("Should have raised.")


@pytest.mark.parametrize(
    "format_, value, expected_value",
    [
        ("binary", "some binary file", b"some binary file"),
        ("date", "2000-01-01", datetime.date(year=2000, month=1, day=1)),
        (
            "date-time",
            "2000-01-01T01:01:01",
            datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1),
        ),
    ],
    ids=["binary", "date", "date-time"],
)
@pytest.mark.utility_base
def test_from_dict_string_format(format_, value, expected_value, __init__):
    """
    GIVEN schema with string type and given format
    WHEN model is defined and constructed with from_dict using the given value
    THEN the instance has the given expected value.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key": {"type": "string", "format": format_}}},
            "__init__": __init__,
        },
    )
    dictionary = {"key": value}

    instance = model.from_dict(**dictionary)

    assert instance.key == expected_value  # pylint: disable=no-member


@pytest.mark.utility_base
def test_from_dict_backref(__init__):
    """
    GIVEN schema with backref which references a model that has been mocked and
        dictionary
    WHEN from_dict is called with the dictionary
    THEN MalformedModelDictionaryError is raised.
    """
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

    with pytest.raises(exceptions.MalformedModelDictionaryError):
        model.from_dict(**{"key_1": 1, "key_2": {"obj_key": "obj value"}})


@pytest.mark.utility_base
def test_from_dict_inheritance_inherits_bool(__init__):
    """
    GIVEN schema where x-inherits is a boolean
    WHEN model is defined and constructed with from_dict
    THEN MalformedSchemaError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key": {"type": "string"}}, "x-inherits": True},
            "__init__": __init__,
        },
    )

    with pytest.raises(exceptions.MalformedSchemaError):
        model.from_dict(**{"key": "value"})


@pytest.mark.utility_base
def test_from_dict_inheritance_model_undefined(__init__):
    """
    GIVEN schema that inherits where parent is not on the models
    WHEN from_dict is called
    THEN SchemaNotFoundError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "string"}},
                "x-inherits": "Parent",
            },
            "__init__": __init__,
        },
    )

    with pytest.raises(exceptions.SchemaNotFoundError):
        model.from_dict(**{"key": "value"})


@pytest.mark.utility_base
def test_from_dict_inheritance_call(mocked_facades_models, __init__):
    """
    GIVEN schema with parent model that has been mocked and dictionary
    WHEN from_dict is called with the dictionary
    THEN from_dict on the mocked model is called with the portion of the dictionary
        for that model.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "string"}},
                "x-inherits": "Parent",
            },
            "__init__": __init__,
        },
    )

    model.from_dict(**{"key": "value", "parent_key": "parent value"})

    mocked_facades_models.get_model.assert_called_once_with(name="Parent")
    check_func = mocked_facades_models.get_model.return_value.construct_from_dict_init
    check_func.assert_called_once_with(**{"parent_key": "parent value"})


@pytest.mark.utility_base
def test_from_dict_inheritance_return(mocked_facades_models, __init__):
    """
    GIVEN schema with parent model that has been mocked and dictionary
    WHEN from_dict is called with the dictionary
    THEN the from_dict on the mocked model return value is merged with the from_dict for
        the child.
    """
    return_func = mocked_facades_models.get_model.return_value.construct_from_dict_init
    return_func.return_value = {"parent_key": "parent value"}
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "string"}},
                "x-inherits": "Parent",
            },
            "__init__": __init__,
        },
    )

    instance = model.from_dict(**{"key": "value", "parent_key": "parent value"})

    mocked_facades_models.get_model.assert_called_once_with(name="Parent")
    assert instance.key == "value"  # pylint: disable=no-member
    assert instance.parent_key == "parent value"  # pylint: disable=no-member


@pytest.mark.parametrize(
    "value",
    [1, "hi", '"hi"', '{"key_2": 2}'],
    ids=["not string", "invalid JSON", "not dictionary", "invalid dictionary"],
)
@pytest.mark.utility_base
def test_from_str_invalid(__init__, value):
    """
    GIVEN schema and invalid JSON string
    WHEN model is defined with the schema and constructed with from_str
    THEN MalformedModelDictionaryError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key_1": {"type": "integer"}}},
            "__init__": __init__,
        },
    )

    with pytest.raises(exceptions.MalformedModelDictionaryError):
        model.from_str(value)


@pytest.mark.utility_base
def test_from_str(__init__):
    """
    GIVEN schema and JSON string
    WHEN model is defined with the schema and constructed with from_str
    THEN the instance has the properties from the JSON string.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key_1": {"type": "integer"}}},
            "__init__": __init__,
        },
    )

    instance = model.from_str('{"key_1": 1}')

    assert getattr(instance, "key_1") == 1
