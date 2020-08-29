"""Tests for cleaner helpers."""

import pytest

from open_alchemy.schemas.helpers import clean


@pytest.mark.parametrize(
    "schema, expected_schema",
    [
        pytest.param(
            {},
            {},
            id="empty",
        ),
        pytest.param(
            {"key": "value"},
            {"key": "value"},
            id="single not extension",
        ),
        pytest.param(
            {"x-key": "value"},
            {},
            id="single extension",
        ),
        pytest.param(
            {"key_1": "value 1", "key_2": "value 2"},
            {"key_1": "value 1", "key_2": "value 2"},
            id="multiple not extension",
        ),
        pytest.param(
            {"x-key_1": "value 1", "key_2": "value 2"},
            {"key_2": "value 2"},
            id="multiple first extension",
        ),
        pytest.param(
            {"key_1": "value 1", "x-key_2": "value 2"},
            {"key_1": "value 1"},
            id="multiple second extension",
        ),
        pytest.param(
            {"x-key_1": "value 1", "x-key_2": "value 2"},
            {},
            id="multiple all extension",
        ),
    ],
)
@pytest.mark.schemas
@pytest.mark.helper
def test_extension(schema, expected_schema):
    """
    GIVEN schema and expected schema
    WHEN extension is called with the schema
    THEN the expected schema is returned.
    """
    clean.extension(schema=schema)

    assert schema == expected_schema
