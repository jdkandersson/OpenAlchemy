"""Fixtures for utility base tests."""

import pytest


@pytest.fixture
def __init__():
    """Utility base init function."""

    def __init__(self, **kwargs):
        """Construct."""
        for name, value in kwargs.items():
            setattr(self, name, value)

    return __init__
