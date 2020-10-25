"""Tests for value helpers."""

import pytest

from open_alchemy.helpers import peek
from open_alchemy.schemas.validation.helpers import value

CHECK_MATCHES_TESTS = [
    pytest.param(
        {},
        {},
        {},
        peek.format_,
        None,
        id="actual not defined expected not defined",
    ),
    pytest.param(
        {},
        {"format": "format 1"},
        {},
        peek.format_,
        ("expected", '"format 1"', "actual", "not to be defined"),
        id="actual not defined expected defined",
    ),
    pytest.param(
        {"format": "format 1"},
        {},
        {},
        peek.format_,
        ("expected", "not defined", "actual", '"format 1"'),
        id="actual defined expected not defined",
    ),
    pytest.param(
        {"format": "format 1"},
        {"format": "format 2"},
        {},
        peek.format_,
        ("expected", '"format 2"', "actual", '"format 1"'),
        id="actual defined expected defined different",
    ),
    pytest.param(
        {"format": "format 1"},
        {"format": "format 1"},
        {},
        peek.format_,
        None,
        id="actual defined expected defined same",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"format": "format 1"},
        {"RefSchema": {"format": "format 1"}},
        peek.format_,
        None,
        id="$ref actual defined expected defined same",
    ),
    pytest.param(
        {"format": "format 1"},
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"format": "format 1"}},
        peek.format_,
        None,
        id="actual defined $ref expected defined same",
    ),
    pytest.param(
        {"allOf": [{"format": "format 1"}]},
        {"format": "format 1"},
        {},
        peek.format_,
        None,
        id="allOf actual defined expected defined same",
    ),
    pytest.param(
        {"format": "format 1"},
        {"allOf": [{"format": "format 1"}]},
        {},
        peek.format_,
        None,
        id="actual defined allOf expected defined same",
    ),
    pytest.param(
        {"allOf": [{"format": "format 1"}, {"$ref": "#/components/schemas/RefSchema"}]},
        {"format": "format 1"},
        {"RefSchema": {"format": "ref_format"}},
        peek.format_,
        None,
        id="actual defined local ref local first expected defined same",
    ),
    pytest.param(
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"format": "format 1"}]},
        {"format": "format 1"},
        {"RefSchema": {"format": "ref_format"}},
        peek.format_,
        None,
        id="actual defined local ref ref first expected defined same",
    ),
    pytest.param(
        {"format": "format 1"},
        {"allOf": [{"format": "format 1"}, {"$ref": "#/components/schemas/RefSchema"}]},
        {"RefSchema": {"format": "ref_format"}},
        peek.format_,
        None,
        id="actual defined expected defined same local ref local first",
    ),
    pytest.param(
        {"format": "format 1"},
        {"allOf": [{"$ref": "#/components/schemas/RefSchema"}, {"format": "format 1"}]},
        {"RefSchema": {"format": "ref_format"}},
        peek.format_,
        None,
        id="actual defined expected defined same local ref ref first",
    ),
    pytest.param(
        {"x-foreign-key": "foreign.key_1"},
        {"x-foreign-key": "foreign.key_2"},
        {},
        peek.foreign_key,
        ("expected", '"foreign.key_2"', "actual", '"foreign.key_1"'),
        id="other func actual defined expected defined different",
    ),
    pytest.param(
        {"format": "format 1", "key": "value 1"},
        {"format": "format 1", "key": "value 2"},
        {},
        peek.format_,
        None,
        id="unrelated different",
    ),
]


@pytest.mark.parametrize(
    "reference_schema, check_schema, schemas, func, expected_results",
    CHECK_MATCHES_TESTS,
)
@pytest.mark.schemas
@pytest.mark.validate
@pytest.mark.helper
def test_check_matches(reference_schema, check_schema, schemas, func, expected_results):
    """
    GIVEN reference and check schema, schemas, function to get value and expected
        result
    WHEN check_matches is called with the reference and check schema, schemas, function
        to get value
    THEN the expected result is returned.
    """
    returned_result = value.check_matches(
        func=func,
        reference_schema=reference_schema,
        check_schema=check_schema,
        schemas=schemas,
    )

    if expected_results is not None:
        for expected_result in expected_results:
            assert expected_result in returned_result
