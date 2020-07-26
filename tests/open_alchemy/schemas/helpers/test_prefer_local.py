"""Test for prefer local helpers."""

import pytest

from open_alchemy.helpers import peek
from open_alchemy.schemas import helpers


@pytest.mark.parametrize(
    "schema, schemas, expected_value",
    [
        pytest.param({}, {}, None, id="not found",),
        pytest.param({"x-backref": "schema"}, {}, "schema", id="present locally",),
        pytest.param({"allOf": []}, {}, None, id="not present locally in allOf",),
        pytest.param(
            {"allOf": [{"x-backref": "schema"}]},
            {},
            "schema",
            id="present locally in allOf",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {}},
            None,
            id="not present behind $ref",
        ),
        pytest.param(
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"x-backref": "schema"}},
            "schema",
            id="present behind $ref",
        ),
        pytest.param(
            {
                "allOf": [
                    {"x-backref": "schema"},
                    {"$ref": "#/components/schemas/RefSchema"},
                ]
            },
            {"RefSchema": {"x-backref": "wrong_schema"}},
            "schema",
            id="present locally in allOf and behind $ref",
        ),
    ],
)
@pytest.mark.schemas
def test_get(schema, schemas, expected_value):
    """
    GIVEN schema, schemas and expected value
    WHEN get is called with the backref peek helper and the schema and schemas
    THEN the expected value is returned.
    """
    returned_value = helpers.prefer_local.get(
        get_value=peek.backref, schema=schema, schemas=schemas
    )

    assert returned_value == expected_value
