"""Tests for calculate_nullable."""

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "required, generated, nullable, expected_result",
    [
        (None, False, None, True),
        (None, False, False, False),
        (None, False, True, True),
        (None, True, None, False),
        (None, True, False, False),
        (None, True, True, True),
        (False, False, None, True),
        (False, False, False, False),
        (False, False, True, True),
        (False, True, None, False),
        (False, True, False, False),
        (False, True, True, True),
        (True, False, None, False),
        (True, False, False, False),
        (True, False, True, True),
        (True, True, None, False),
        (True, True, False, False),
        (True, True, True, True),
    ],
    ids=[
        "required not given generated False nullable not given",
        "required not given generated False nullable reset",
        "required not given generated False nullable set",
        "required not given generated True  nullable not given",
        "required not given generated True  nullable reset",
        "required not given generated True  nullable set",
        "required reset     generated False nullable not given",
        "required reset     generated False nullable reset",
        "required reset     generated False nullable set",
        "required reset     generated True  nullable not given",
        "required reset     generated True  nullable reset",
        "required reset     generated True  nullable set",
        "required set       generated False nullable not given",
        "required set       generated False nullable reset",
        "required set       generated False nullable set",
        "required set       generated True  nullable not given",
        "required set       generated True  nullable reset",
        "required set       generated True  nullable set",
    ],
)
@pytest.mark.helper
def test_calculate_nullable(required, generated, nullable, expected_result):
    """
    GIVEN required, nullable and expected result
    WHEN calculate_nullable is called with nullable and required
    THEN the expected result is returned.
    """
    result = helpers.calculate_nullable(
        nullable=nullable, generated=generated, required=required
    )

    assert result == expected_result
