"""Tests for UtilityBase."""

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
