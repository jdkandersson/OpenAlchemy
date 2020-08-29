"""Test for the repr of the model."""

from unittest import mock

import pytest

from open_alchemy import utility_base


class Model:
    """Model class for testing."""

    def __init__(self):
        """Construct."""
        self.property_int = 1
        self.property_str = "value 1"
        self.property_repr = mock.MagicMock(
            spec=["__repr__"], __repr__=lambda _: "open_alchemy.models.RefModel()"
        )


@pytest.mark.parametrize(
    "properties, expected_repr",
    [
        pytest.param(
            {},
            "open_alchemy.models.Model()",
            id="no properties",
        ),
        pytest.param(
            {"property_not_def": {}},
            "open_alchemy.models.Model(property_not_def=None)",
            id="single property property simple no value",
        ),
        pytest.param(
            {"property_int": {}},
            "open_alchemy.models.Model(property_int=1)",
            id="single property property simple value",
        ),
        pytest.param(
            {"property_repr": {}},
            "open_alchemy.models.Model(property_repr=open_alchemy.models.RefModel())",
            id="single property property repr",
        ),
        pytest.param(
            {"property_int": {}, "property_str": {}},
            "open_alchemy.models.Model(property_int=1, property_str='value 1')",
            id="multiple property property",
        ),
    ],
)
@pytest.mark.utility_base
def test_calculate(properties, expected_repr):
    """
    GIVEN model instance, properties and expected repr result
    WHEN calculate is called on the instance
    THEN the expected repr is returned.
    """
    instance = Model()

    returned_repr = utility_base.repr_.calculate(
        instance=instance, properties=properties
    )

    assert returned_repr == expected_repr
