"""Tests for calculate_nullable."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "required, nullable, expected_result",
    [
        (None, None, True),
        (None, False, False),
        (None, True, True),
        (False, None, True),
        (False, False, False),
        (False, True, True),
        (True, None, False),
        (True, False, False),
        (True, True, True),
    ],
    ids=[
        "required not given nullable not given",
        "required not given nullable reset",
        "required not given nullable set",
        "required reset nullable not given",
        "required reset nullable reset",
        "required reset nullable set",
        "required set nullable not given",
        "required set nullable reset",
        "required set nullable set",
    ],
)
@pytest.mark.helper
def test_calculate_nullable(required, nullable, expected_result):
    """
    GIVEN required, nullable and expected result
    WHEN calculate_nullable is called with nullable and required
    THEN the expected result is returned.
    """
    result = helpers.calculate_nullable(nullable=nullable, required=required)

    assert result == expected_result
