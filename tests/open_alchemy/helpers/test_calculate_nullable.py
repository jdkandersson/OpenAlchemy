"""Tests for calculate_nullable."""

import pytest

from open_alchemy.helpers import calculate_nullable


@pytest.mark.parametrize(
    "required, generated, defaulted, nullable, expected_result",
    [
        (None, False, False, None, True),
        (None, False, False, False, False),
        (None, False, False, True, True),
        (None, False, True, None, False),
        (None, False, True, False, False),
        (None, False, True, True, True),
        (None, True, False, None, False),
        (None, True, False, False, False),
        (None, True, False, True, True),
        (None, True, True, None, False),
        (None, True, True, False, False),
        (None, True, True, True, True),
        (False, False, False, None, True),
        (False, False, False, False, False),
        (False, False, False, True, True),
        (False, False, True, None, False),
        (False, False, True, False, False),
        (False, False, True, True, True),
        (False, True, False, None, False),
        (False, True, False, False, False),
        (False, True, False, True, True),
        (False, True, True, None, False),
        (False, True, True, False, False),
        (False, True, True, True, True),
        (True, False, False, None, False),
        (True, False, False, False, False),
        (True, False, False, True, True),
        (True, False, True, None, False),
        (True, False, True, False, False),
        (True, False, True, True, True),
        (True, True, False, None, False),
        (True, True, False, False, False),
        (True, True, False, True, True),
        (True, True, True, None, False),
        (True, True, True, False, False),
        (True, True, True, True, True),
    ],
    ids=[
        "required not given generated False default not given nullable not given",
        "required not given generated False default not given nullable reset",
        "required not given generated False default not given nullable set",
        "required not given generated False default given     nullable not given",
        "required not given generated False default given     nullable reset",
        "required not given generated False default given     nullable set",
        "required not given generated True  default not given nullable not given",
        "required not given generated True  default not given nullable reset",
        "required not given generated True  default not given nullable set",
        "required not given generated True  default given     nullable not given",
        "required not given generated True  default given     nullable reset",
        "required not given generated True  default given     nullable set",
        "required reset     generated False default not given nullable not given",
        "required reset     generated False default not given nullable reset",
        "required reset     generated False default not given nullable set",
        "required reset     generated False default given     nullable not given",
        "required reset     generated False default given     nullable reset",
        "required reset     generated False default given     nullable set",
        "required reset     generated True  default not given nullable not given",
        "required reset     generated True  default not given nullable reset",
        "required reset     generated True  default not given nullable set",
        "required reset     generated True  default given     nullable not given",
        "required reset     generated True  default given     nullable reset",
        "required reset     generated True  default given     nullable set",
        "required set       generated False default not given nullable not given",
        "required set       generated False default not given nullable reset",
        "required set       generated False default not given nullable set",
        "required set       generated False default given     nullable not given",
        "required set       generated False default given     nullable reset",
        "required set       generated False default given     nullable set",
        "required set       generated True  default not given nullable not given",
        "required set       generated True  default not given nullable reset",
        "required set       generated True  default not given nullable set",
        "required set       generated True  default given     nullable not given",
        "required set       generated True  default given     nullable reset",
        "required set       generated True  default given     nullable set",
    ],
)
@pytest.mark.helper
def test_calculate_nullable(required, generated, defaulted, nullable, expected_result):
    """
    GIVEN required, generated, defaulted, nullable and expected result
    WHEN calculate_nullable is called with nullable, defaulted, generated and required
    THEN the expected result is returned.
    """
    result = calculate_nullable.calculate_nullable(
        nullable=nullable, generated=generated, required=required, defaulted=defaulted
    )

    assert result == expected_result
