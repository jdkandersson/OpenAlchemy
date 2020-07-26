"""Test for iterate helpers."""

import pytest

from open_alchemy.schemas.helpers import iterate


@pytest.mark.parametrize(
    "schemas, expected_schemas",
    [
        pytest.param({}, [], id="empty"),
        pytest.param({"schema_1": {}}, [], id="single not"),
        pytest.param(
            {"schema_1": {"x-tablename": "table 1"}},
            [("schema_1", {"x-tablename": "table 1"})],
            id="single is",
        ),
        pytest.param({"schema_1": {}, "schema_2": {},}, [], id="multiple none"),
        pytest.param(
            {"schema_1": {"x-tablename": "table 1"}, "schema_2": {},},
            [("schema_1", {"x-tablename": "table 1"}),],
            id="multiple first",
        ),
        pytest.param(
            {"schema_1": {}, "schema_2": {"x-tablename": "table 2"},},
            [("schema_2", {"x-tablename": "table 2"}),],
            id="multiple last",
        ),
        pytest.param(
            {
                "schema_1": {"x-tablename": "table 1"},
                "schema_2": {"x-tablename": "table 2"},
            },
            [
                ("schema_1", {"x-tablename": "table 1"}),
                ("schema_2", {"x-tablename": "table 2"}),
            ],
            id="multiple all",
        ),
    ],
)
@pytest.mark.schemas
def test_constructable(schemas, expected_schemas):
    """
    GIVEN schemas and expected schemas
    WHEN constructable is called with the schemas
    THEN an iterable with all the names and schemas in the expected schemas are
        returned.
    """
    returned_schemas = iterate.constructable(schemas=schemas)

    assert list(returned_schemas) == expected_schemas
