"""Tests for object conversion to a dictionary."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import utility_base


class TestConvertRelationship:
    """Tests for _convert_relationship."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.utility_base
    def test_no_to_dict():
        """
        GIVEN value that does not have to_dict
        WHEN _convert_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        value = mock.MagicMock()
        del value.to_dict

        with pytest.raises(exceptions.InvalidModelInstanceError):
            utility_base.to_dict.object_._convert_relationship(value=value)

    @staticmethod
    @pytest.mark.utility_base
    def test_expects_args():
        """
        GIVEN value that has a to_dict function that expects arguments
        WHEN _convert_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        object_value_expects_args = mock.MagicMock()

        def to_dict_with_args(test):
            """to_dict function that expects arguments."""
            raise AssertionError(f"Should not have been called with {test}")

        object_value_expects_args.to_dict = to_dict_with_args

        with pytest.raises(exceptions.InvalidModelInstanceError):
            utility_base.to_dict.object_._convert_relationship(
                value=object_value_expects_args
            )

    @staticmethod
    @pytest.mark.utility_base
    def test_valid():
        """
        GIVEN value that has a to_dict function
        WHEN _convert_relationship is called with the value
        THEN to_dict is called and it's return value is returned.
        """
        object_value = mock.MagicMock()

        returned_value = utility_base.to_dict.object_._convert_relationship(
            value=object_value
        )

        object_value.to_dict.assert_called_once_with()  # pylint: disable=no-member
        expected_return_value = (
            object_value.to_dict.return_value  # pylint: disable=no-member
        )
        assert returned_value == expected_return_value

    @staticmethod
    @pytest.mark.utility_base
    def test_valid_none():
        """
        GIVEN None value
        WHEN _convert_relationship is called with the value
        THEN None is returned.
        """
        returned_value = utility_base.to_dict.object_._convert_relationship(value=None)

        assert returned_value is None


class TestConvertReadOnly:
    """Tests for _convert_read_only."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, exception",
        [
            ({}, exceptions.MalformedSchemaError),
            ({"properties": 1}, exceptions.MalformedSchemaError),
            ({"properties": {}}, exceptions.MalformedSchemaError),
        ],
        ids=["no properties", "properties not dict", "empty properties"],
    )
    @pytest.mark.utility_base
    def test_invalid(schema, exception):
        """
        GIVEN schema that is not valid and expected exception
        WHEN _convert_read_only is called with the schema
        THEN the expected exception is raised.
        """
        with pytest.raises(exception):
            utility_base.to_dict.object_._convert_read_only(
                schema=schema, value=mock.MagicMock()
            )

    @staticmethod
    @pytest.mark.parametrize(
        "schema, value, expected_value",
        [
            ({"properties": {"key": "type 1"}}, mock.MagicMock(spec=[]), {"key": None}),
            ({"properties": {"key": "type 1"}}, None, None),
            (
                {"properties": {"key": "type 1"}},
                mock.MagicMock(spec=["key"], key="value"),
                {"key": "value"},
            ),
            (
                {"properties": {"key_1": "type 1", "key_2": "type 2"}},
                mock.MagicMock(spec=[]),
                {"key_1": None, "key_2": None},
            ),
            (
                {"properties": {"key_1": "type 1", "key_2": "type 2"}},
                mock.MagicMock(spec=["key_1"], key_1="value 1"),
                {"key_1": "value 1", "key_2": None},
            ),
            (
                {"properties": {"key_1": "type 1", "key_2": "type 2"}},
                mock.MagicMock(
                    spec=["key_1", "key_2"], key_1="value 1", key_2="value 2"
                ),
                {"key_1": "value 1", "key_2": "value 2"},
            ),
        ],
        ids=[
            "None",
            "single property missing",
            "single property present",
            "multiple property missing",
            "multiple property some present",
            "multiple property present",
        ],
    )
    @pytest.mark.utility_base
    def test_valid(schema, value, expected_value):
        """
        GIVEN schema, value and expected value
        WHEN _convert_read_only is called with the schema and value
        THEN the expected value is returned..
        """
        returned_value = utility_base.to_dict.object_._convert_read_only(
            schema=schema, value=value
        )

        assert returned_value == expected_value


@pytest.mark.parametrize(
    "schema, value, read_only",
    [
        (
            {"properties": {"key": "type 1"}},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            None,
        ),
        (
            {"properties": {"key": "type 1"}},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            False,
        ),
        ({"properties": {"key": "type 1"}}, mock.MagicMock(key="value"), True),
        (
            {"properties": {"key": "type 1"}, "readOnly": False},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            None,
        ),
        (
            {"properties": {"key": "type 1"}, "readOnly": True},
            mock.MagicMock(key="value"),
            None,
        ),
        (
            {"properties": {"key": "type 1"}, "readOnly": False},
            mock.MagicMock(to_dict=lambda: {"key": "value"}),
            False,
        ),
        (
            {"properties": {"key": "type 1"}, "readOnly": True},
            mock.MagicMock(key="value"),
            False,
        ),
    ],
    ids=[
        "readOnly arg None",
        "readOnly arg False",
        "readOnly arg True",
        "readOnly arg None  schema False",
        "readOnly arg None  schema True",
        "readOnly arg False schema False",
        "readOnly arg False schema True",
    ],
)
@pytest.mark.utility_base
def test_convert(schema, value, read_only):
    """
    GIVEN schema, value and readOnly value
    WHEN convert is called with the schema, value and readOnly
    THEN the dictionary is returned.
    """
    return_value = utility_base.to_dict.object_.convert(
        schema=schema, value=value, read_only=read_only
    )

    assert return_value == {"key": "value"}
