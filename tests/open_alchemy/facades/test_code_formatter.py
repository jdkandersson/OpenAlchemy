"""Tests for code formatting."""

import pytest

from open_alchemy import facades


@pytest.mark.parametrize(
    "source, expected_source",
    [pytest.param('"test"\n', '"test"\n', id="no formatting")],
)
@pytest.mark.facade
@pytest.mark.code_formatter
def test_apply(source, expected_source):
    """
    GIVEN source code and expected source code
    WHEN apply is called with the source code
    THEN the expected source code is returned.
    """
    returned_source = facades.code_formatter.apply(source=source)

    assert returned_source == expected_source
