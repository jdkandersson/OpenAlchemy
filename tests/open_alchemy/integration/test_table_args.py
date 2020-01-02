"""Integration tests."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.parametrize(
    "schema_additions, sql, expected_contents",
    [
        (
            {"x-composite-unique": ["id"]},
            "SELECT sql FROM sqlite_master WHERE name='table'",
            ["UNIQUE (id)"],
        ),
        (
            {"x-composite-unique": [["id"], ["column"]]},
            "SELECT sql FROM sqlite_master WHERE name='table'",
            ["UNIQUE (id)", 'UNIQUE ("column")'],
        ),
        (
            {"x-composite-unique": {"columns": ["id"]}},
            "SELECT sql FROM sqlite_master WHERE name='table'",
            ["UNIQUE (id)"],
        ),
        (
            {"x-composite-unique": {"name": "id", "columns": ["id"]}},
            "SELECT sql FROM sqlite_master WHERE name='table'",
            ["CONSTRAINT id UNIQUE (id)"],
        ),
        (
            {"x-composite-unique": [{"columns": ["id"]}, {"columns": ["column"]}]},
            "SELECT sql FROM sqlite_master WHERE name='table'",
            ["UNIQUE (id)", 'UNIQUE ("column")'],
        ),
        (
            {"x-composite-index": ["id"]},
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ['INDEX ix_table_id ON "table" (id)'],
        ),
        (
            {"x-composite-index": [["id"], ["column"]]},
            "SELECT sql FROM sqlite_master WHERE type='index'",
            [
                'INDEX ix_table_id ON "table" (id)',
                'INDEX ix_table_column ON "table" ("column")',
            ],
        ),
        (
            {"x-composite-index": {"expressions": ["id"]}},
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ['INDEX ix_table_id ON "table" (id)'],
        ),
        (
            {"x-composite-index": {"name": "id", "expressions": ["id"]}},
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ['INDEX id ON "table" (id)'],
        ),
        (
            {"x-composite-index": {"expressions": ["id"], "unique": True}},
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ['UNIQUE INDEX ix_table_id ON "table" (id)'],
        ),
        (
            {
                "x-composite-index": [
                    {"expressions": ["id"]},
                    {"expressions": ["column"]},
                ]
            },
            "SELECT sql FROM sqlite_master WHERE type='index'",
            [
                'INDEX ix_table_id ON "table" (id)',
                'INDEX ix_table_column ON "table" ("column")',
            ],
        ),
    ],
    ids=[
        "unique array",
        "unique multiple array",
        "unique object",
        "unique object name",
        "unique multiple object",
        "index array single",
        "index multiple array",
        "index object",
        "index object name",
        "index object unique",
        "index multiple object",
    ],
)
@pytest.mark.integration
def test_table_args_unique(engine, schema_additions, sql, expected_contents):
    """
    GIVEN schema, additional properties for schema, sql to execute and expected
        contents
    WHEN models are constructed
    THEN when sql is executed the expected contents are in the result.
    """
    # Defining schema
    spec = {
        "components": {
            "schemas": {
                "Table": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "column": {"type": "integer"},
                    },
                    "x-tablename": "table",
                    "type": "object",
                    **schema_additions,
                }
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model_factory(name="Table")

    # Creating models
    base.metadata.create_all(engine)

    # Query schema
    results_list = list(str(result) for result in engine.execute(sql))
    results = "\n".join(results_list)
    for expected_content in expected_contents:
        assert expected_content in results
