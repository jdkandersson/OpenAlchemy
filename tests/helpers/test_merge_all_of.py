"""Tests for merge allOf helper."""


import pytest

from openapi_sqlalchemy import helpers


@pytest.mark.helper
def test_not_all_of():
    """
    GIVEN spec that does not have the allOf statement
    WHEN merge_all_of is called with the spec
    THEN the spec is returned.
    """
    spec = {"key": "value"}

    return_spec = helpers.merge_all_of(spec=spec)

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_all_of_single():
    """
    GIVEN spec that has allOf statement with a single spec
    WHEN merge_all_of is called with the spec
    THEN the spec in allOf is returned.
    """
    spec = {"allOf": [{"key": "value"}]}

    return_spec = helpers.merge_all_of(spec=spec)

    assert return_spec == {"key": "value"}


@pytest.mark.helper
def test_all_of_multiple():
    """
    GIVEN spec that has multiple specs under allOf
    WHEN merge_all_of is called with the spec
    THEN the merged spec of all specs under allOf is returned.
    """
    spec = {"allOf": [{"key_1": "value_1"}, {"key_2": "value_2"}]}

    return_spec = helpers.merge_all_of(spec=spec)

    assert return_spec == {"key_1": "value_1", "key_2": "value_2"}
