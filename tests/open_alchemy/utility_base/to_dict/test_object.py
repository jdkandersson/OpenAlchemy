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
    def to_dict_with_args(test):
        """to_dict function that expects arguments."""
        raise AssertionError(f"Should not have been called with {test}")

    @classmethod
    @pytest.mark.utility_base
    def test_expects_args(cls):
        """
        GIVEN value that has a to_dict function that expects arguments
        WHEN _convert_relationship is called with the value
        THEN InvalidModelInstanceError is raised.
        """
        value = mock.MagicMock()
        value.to_dict = cls.to_dict_with_args

        with pytest.raises(exceptions.InvalidModelInstanceError):
            utility_base.to_dict.object_._convert_relationship(value=value)

    @staticmethod
    @pytest.mark.utility_base
    def test_valid():
        """
        GIVEN value that has a to_dict function
        WHEN _convert_relationship is called with the value
        THEN to_dict is called and it's return value is returned.
        """
        value = mock.MagicMock()

        returned_value = utility_base.to_dict.object_._convert_relationship(value=value)

        value.to_dict.assert_called_once_with()
        assert returned_value == value.to_dict.return_value
