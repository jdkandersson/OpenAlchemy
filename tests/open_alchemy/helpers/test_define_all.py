"""Tests for define_all helper."""

from unittest import mock

import pytest

from open_alchemy import helpers


@pytest.mark.parametrize(
    "schemas, expected_calls",
    [
        ({}, []),
        ({"Table": {}}, []),
        ({"Table": {"x-tablename": "table"}}, ["Table"]),
        ({"Table": {"allOf": [{"x-tablename": "table"}]}}, ["Table"]),
        (
            {
                "Table": {"x-tablename": "table"},
                "RefTable": {"$ref": "#/components/schemas/Table"},
            },
            ["Table"],
        ),
        ({"Table1": {}, "Table2": {}}, []),
        ({"Table1": {"x-tablename": "table1"}, "Table2": {}}, ["Table1"]),
        ({"Table1": {}, "Table2": {"x-tablename": "table2"}}, ["Table2"]),
        (
            {"Table1": {"x-tablename": "table1"}, "Table2": {"x-tablename": "table2"}},
            ["Table1", "Table2"],
        ),
    ],
    ids=[
        "empty,                          zero",
        "single no x-tablename,          zero",
        "single x-tablename,             one",
        "allOf single x-tablename,       one",
        "$ref single x-tablename,        one",
        "multiple no x-tablename,        multiple",
        "multiple one first x-tablename, multiple",
        "multiple one last x-tablename, multiple",
        "multiple all x-tablename,       multiple",
    ],
)
@pytest.mark.helper
def test_call(schemas, expected_calls):
    """
    GIVEN mocked model factory, schemas and expected calls
    WHEN define_all is called with the model factory and schemas
    THEN the mocked model factory has the expected calls.
    """
    model_factory = mock.MagicMock()

    helpers.define_all(model_factory=model_factory, schemas=schemas)

    assert model_factory.call_count == len(expected_calls)
    for name in expected_calls:
        model_factory.assert_any_call(name=name)


@pytest.mark.helper
def test_remote_ref(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref that is not normalized and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the schemas are stored under the normalized path.
    """
    # pylint: disable=protected-access
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Table": {"key": "value"}}')
    # Set up remote schemas store
    helpers.ref._remote_schema_store.spec_context = str(schemas_file)
    schemas = {"RefTable": {"$ref": "remote.json#/Table"}}
    model_factory = mock.MagicMock()

    helpers.define_all(model_factory=model_factory, schemas=schemas)
