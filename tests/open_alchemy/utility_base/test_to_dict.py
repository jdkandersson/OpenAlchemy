"""Tests for UtilityBase."""

import datetime
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


@pytest.mark.utility_base
def test_to_dict_no_type(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with a property without a
        type
    WHEN to_dict is called
    THEN MalformedSchemaError is raised.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {}}}, "__init__": __init__},
    )
    instance = model()

    with pytest.raises(exceptions.TypeMissingError):
        instance.to_dict()


@pytest.mark.parametrize(
    "schema, init_args, expected_dict",
    [
        ({"properties": {}}, {}, {}),
        ({"properties": {}}, {"key_1": "value 1"}, {}),
        ({"properties": {"key_1": {"type": "type 1"}}}, {}, {"key_1": None}),
        (
            {"properties": {"key_1": {"type": "type 1"}}},
            {"key_1": "value 1"},
            {"key_1": "value 1"},
        ),
        (
            {"properties": {"key_1": {"type": "type 1"}, "key_2": {"type": "type 2"}}},
            {"key_1": "value 1", "key_2": "value 2"},
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
def test_to_dict_simple_type(schema, init_args, expected_dict, __init__):
    """
    GIVEN class that derives from UtilityBase with a given schema with properties that
        are not objects and expected object
    WHEN to_dict is called
    THEN the expected object is returned.
    """
    model = type(
        "model", (utility_base.UtilityBase,), {"_schema": schema, "__init__": __init__}
    )
    instance = model(**init_args)

    returned_dict = instance.to_dict()

    assert returned_dict == expected_dict


@pytest.mark.utility_base
def test_to_str(__init__):
    """
    GIVEN class that derives from UtilityBase with a given schema with properties
    WHEN to_str is called
    THEN the JSON representation of the properties is returned.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {"properties": {"key_1": {"type": "type 1"}}},
            "__init__": __init__,
        },
    )
    instance = model(key_1=1)

    returned_str = instance.to_str()

    assert returned_str == '{"key_1": 1}'


@pytest.mark.parametrize("init_kwargs", [{}, {"key": None}], ids=["undefined", "none"])
@pytest.mark.utility_base
def test_to_dict_object_none(init_kwargs, __init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an object property and
        init args
    WHEN model is initialized with init_args and to_dict is called
    THEN None is returned for the property.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}, "__init__": __init__},
    )
    instance = model(**init_kwargs)

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": None}


@pytest.mark.utility_base
def test_to_dict_object(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an object property
        that has a mock model
    WHEN to_dict is called
    THEN the mock model to_dict return value is returned as the property value.
    """
    mock_model = mock.MagicMock()
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {"_schema": {"properties": {"key": {"type": "object"}}}, "__init__": __init__},
    )
    instance = model(**{"key": mock_model})

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": mock_model.to_dict.return_value}


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


@pytest.mark.parametrize("init_kwargs", [{}, {"key": None}], ids=["undefined", "none"])
@pytest.mark.utility_base
def test_to_dict_array_none(init_kwargs, __init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an array property and
        init args
    WHEN model is initialized with init_args and to_dict is called
    THEN an empty list is returned for the property.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "array", "items": {"type": "object"}}}
            },
            "__init__": __init__,
        },
    )
    instance = model(**init_kwargs)

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": []}


@pytest.mark.utility_base
def test_to_dict_array_empty(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an array property
        that is empty
    WHEN to_dict is called
    THEN an empty list is returned as the property value.
    """
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "array", "items": {"type": "object"}}}
            },
            "__init__": __init__,
        },
    )
    instance = model(**{"key": []})

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": []}


@pytest.mark.utility_base
def test_to_dict_array_single(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an array property
        that has a single mock model
    WHEN to_dict is called
    THEN list with the mock model to_dict return value is returned as the property
        value.
    """
    mock_model = mock.MagicMock()
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "array", "items": {"type": "object"}}}
            },
            "__init__": __init__,
        },
    )
    instance = model(**{"key": [mock_model]})

    returned_dict = instance.to_dict()

    assert returned_dict == {"key": [mock_model.to_dict.return_value]}


@pytest.mark.utility_base
def test_to_dict_array_multiple(__init__):
    """
    GIVEN class that derives from UtilityBase with a schema with an array property
        that has multiple mock models
    WHEN to_dict is called
    THEN list with the mock models to_dict return value is returned as the property
        value.
    """
    mock_models = [mock.MagicMock(), mock.MagicMock()]
    model = type(
        "model",
        (utility_base.UtilityBase,),
        {
            "_schema": {
                "properties": {"key": {"type": "array", "items": {"type": "object"}}}
            },
            "__init__": __init__,
        },
    )
    instance = model(**{"key": mock_models})

    returned_dict = instance.to_dict()

    assert returned_dict == {
        "key": list(
            map(lambda mock_model: mock_model.to_dict.return_value, mock_models)
        )
    }


class TestObjectToDictRelationship:
    """Tests _object_to_dict_relationship."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.utility_base
    def test_object_to_dict_relationship_object_no_to_dict():
        """
        GIVEN value that has a to_dict function that raises AttributeError
        WHEN _object_to_dict_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        value = mock.MagicMock()
        value.to_dict.side_effect = AttributeError

        with pytest.raises(exceptions.InvalidModelInstanceError):
            utility_base.UtilityBase._object_to_dict_relationship(
                value=value, name="name 1"
            )

    @staticmethod
    @pytest.mark.utility_base
    def test_object_to_dict_relationship_object_to_dict_relationship_different_func():
        """
        GIVEN value that has a to_dict function that raises TypeError
        WHEN _object_to_dict_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        value = mock.MagicMock()
        value.to_dict.side_effect = TypeError

        with pytest.raises(exceptions.InvalidModelInstanceError):
            utility_base.UtilityBase._object_to_dict_relationship(
                value=value, name="name 1"
            )

    @staticmethod
    @pytest.mark.utility_base
    def test_object_to_dict_relationship_object_to_dict_relationship():
        """
        GIVEN value that has a to_dict function that raises TypeError
        WHEN _object_to_dict_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        value = mock.MagicMock()

        returned_value = utility_base.UtilityBase._object_to_dict_relationship(
            value=value, name="name 1"
        )

        assert returned_value == value.to_dict.return_value
        value.to_dict.assert_called_once_with()


class TestObjectToDictReadOnly:
    """Tests for _object_to_dict_read_only"""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "spec", [{}, {"properties": {}}], ids=["properties missing", "properties empty"]
    )
    @pytest.mark.utility_base
    def test_spec_invalid(spec):
        """
        GIVEN invalid spec
        WHEN _object_to_dict_read_only is called with the spec
        THEN MalformedSchemaError is raised.
        """
        with pytest.raises(exceptions.MalformedSchemaError):
            utility_base.UtilityBase._object_to_dict_read_only(
                spec=spec, value=mock.MagicMock(), name="name 1"
            )

    @staticmethod
    @pytest.mark.utility_base
    def test_missing():
        """
        GIVEN spec and value without key
        WHEN _object_to_dict_read_only is called with the value
        THEN None is returned for the key.
        """
        value = mock.MagicMock()
        del value.key_1
        spec = {"type": "object", "properties": {"key_1": {"type": "string"}}}

        returned_value = utility_base.UtilityBase._object_to_dict_read_only(
            value=value, spec=spec, name="name 1"
        )

        assert returned_value == {"key_1": None}

    @staticmethod
    @pytest.mark.utility_base
    def test_single():
        """
        GIVEN spec with single property and mock value
        WHEN _object_to_dict_read_only is called with the value
        THEN dictionary with values for the key is returned.
        """
        value = mock.MagicMock()
        spec = {"type": "object", "properties": {"key_1": {"type": "string"}}}

        returned_value = utility_base.UtilityBase._object_to_dict_read_only(
            value=value, spec=spec, name="name 1"
        )

        assert returned_value == {"key_1": value.key_1}

    @staticmethod
    @pytest.mark.utility_base
    def test_multiple():
        """
        GIVEN spec with multiple properties and mock value
        WHEN _object_to_dict_read_only is called with the value
        THEN dictionary with values for the key is returned.
        """
        value = mock.MagicMock()
        spec = {
            "type": "object",
            "properties": {"key_1": {"type": "string"}, "key_2": {"type": "string"}},
        }

        returned_value = utility_base.UtilityBase._object_to_dict_read_only(
            value=value, spec=spec, name="name 1"
        )

        assert returned_value == {"key_1": value.key_1, "key_2": value.key_2}


class TestToDictProperty:
    """Tests for _to_dict_property."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "spec, value, error",
        [
            ({}, mock.MagicMock(), exceptions.TypeMissingError),
            ({"type": "array"}, [mock.MagicMock()], exceptions.MalformedSchemaError),
            (
                {"type": "array", "items": {}},
                [mock.MagicMock()],
                exceptions.TypeMissingError,
            ),
            (
                {"type": "array", "items": {"type": "array"}},
                [mock.MagicMock()],
                exceptions.MalformedSchemaError,
            ),
        ],
        ids=["no type", "array no items", "array items no type", "array items array"],
    )
    @pytest.mark.utility_base
    def test_invalid_spec(spec, value, error):
        """
        GIVEN invalid property spec and expected error
        WHEN _to_dict_property is called with the spec
        THEN the expected error is raised.
        """
        with pytest.raises(error):
            utility_base.UtilityBase._to_dict_property(value, spec=spec, name="name 1")

    @staticmethod
    @pytest.mark.parametrize("value", [None, "value 1"], ids=["none", "value"])
    @pytest.mark.utility_base
    def test_simple_value(value):
        """
        GIVEN spec that isn't an object or array and value
        WHEN _to_dict_property is called with the spec and value
        THEN value is returned.
        """
        spec = {"type": "string"}

        returned_value = utility_base.UtilityBase._to_dict_property(
            value, spec=spec, name="name 1"
        )

        assert returned_value == value

    @staticmethod
    @pytest.mark.parametrize(
        "format_, value, expected_value",
        [
            ("binary", b"some binary file", "some binary file"),
            ("date", datetime.date(year=2000, month=1, day=1), "2000-01-01"),
            (
                "date-time",
                datetime.datetime(
                    year=2000, month=1, day=1, hour=1, minute=1, second=1
                ),
                "2000-01-01T01:01:01",
            ),
        ],
        ids=["binary", "date", "date-time"],
    )
    @pytest.mark.utility_base
    def test_string_format(format_, value, expected_value):
        """
        GIVEN spec with a string type and given format
        WHEN _to_dict_property is called with the spec and given value
        THEN the given expected value is returned as a string.
        """
        spec = {"type": "string", "format": format_}

        returned_value = utility_base.UtilityBase._to_dict_property(
            value, spec=spec, name="name 1"
        )

        assert returned_value == expected_value

    @staticmethod
    @pytest.mark.utility_base
    def test_object_none():
        """
        GIVEN object spec and None value
        WHEN _to_dict_property is called with the spec and value
        THEN None is returned.
        """
        value = None
        spec = {"type": "object"}

        returned_value = utility_base.UtilityBase._to_dict_property(
            value, spec=spec, name="name 1"
        )

        assert returned_value == value

    @staticmethod
    @pytest.mark.utility_base
    def test_object_value():
        """
        GIVEN object spec and value
        WHEN _to_dict_property is called with the spec and value
        THEN value to_dict return value is returned.
        """
        value = mock.MagicMock()
        spec = {"type": "object"}

        returned_value = utility_base.UtilityBase._to_dict_property(
            value, spec=spec, name="name 1"
        )

        assert returned_value == value.to_dict.return_value

    @staticmethod
    @pytest.mark.utility_base
    def test_array_none():
        """
        GIVEN areray spec and None value
        WHEN _to_dict_property is called with the spec and value
        THEN empty list is returned.
        """
        spec = {"type": "array", "items": {"type": "object"}}

        returned_value = utility_base.UtilityBase._to_dict_property(
            None, spec=spec, name="name 1"
        )

        assert returned_value == []

    @staticmethod
    @pytest.mark.utility_base
    def test_array_empty():
        """
        GIVEN object spec and empty list value
        WHEN _to_dict_property is called with the spec and value
        THEN empty list.
        """
        spec = {"type": "array", "items": {"type": "object"}}

        returned_value = utility_base.UtilityBase._to_dict_property(
            [], spec=spec, name="name 1"
        )

        assert returned_value == []

    @staticmethod
    @pytest.mark.utility_base
    def test_array_single():
        """
        GIVEN object spec and single item list value
        WHEN _to_dict_property is called with the spec and value
        THEN item to_dict value is returned in a list.
        """
        item_value = mock.MagicMock()
        spec = {"type": "array", "items": {"type": "object"}}

        returned_value = utility_base.UtilityBase._to_dict_property(
            [item_value], spec=spec, name="name 1"
        )

        assert returned_value == [item_value.to_dict.return_value]

    @staticmethod
    @pytest.mark.utility_base
    def test_array_multiple():
        """
        GIVEN object spec and multiple item list values
        WHEN _to_dict_property is called with the spec and value
        THEN item to_dict values are returned in a list.
        """
        item1_value = mock.MagicMock()
        item2_value = mock.MagicMock()
        spec = {"type": "array", "items": {"type": "object"}}

        returned_value = utility_base.UtilityBase._to_dict_property(
            [item1_value, item2_value], spec=spec, name="name 1"
        )

        assert returned_value == [
            item1_value.to_dict.return_value,
            item2_value.to_dict.return_value,
        ]

    @staticmethod
    @pytest.mark.utility_base
    def test_read_only():
        """
        GIVEN readOnly spec and mock value
        WHEN _to_dict_property is called with the spec and value
        THEN spec property values are returned.
        """
        value = mock.MagicMock()
        spec = {
            "readOnly": True,
            "type": "object",
            "properties": {"key": {"type": "string"}},
        }

        returned_value = utility_base.UtilityBase._to_dict_property(
            value, spec=spec, name="name 1"
        )

        assert returned_value == {"key": value.key}

    @staticmethod
    @pytest.mark.utility_base
    def test_read_only_array():
        """
        GIVEN readOnly array spec and mock value
        WHEN _to_dict_property is called with the spec and value
        THEN spec property values are returned.
        """
        value = mock.MagicMock()
        spec = {
            "readOnly": True,
            "type": "array",
            "items": {"type": "object", "properties": {"key": {"type": "string"}}},
        }

        returned_value = utility_base.UtilityBase._to_dict_property(
            [value], spec=spec, name="name 1"
        )

        assert returned_value == [{"key": value.key}]
