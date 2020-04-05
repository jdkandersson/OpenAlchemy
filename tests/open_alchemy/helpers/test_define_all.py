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
        (
            {
                "Child": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                "Parent": {"x-tablename": "parent"},
            },
            ["Parent", "Child"],
        ),
        (
            {
                "Parent": {"x-tablename": "parent"},
                "Child": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
            },
            ["Parent", "Child"],
        ),
        (
            {
                "Child": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
                "Parent": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Grandparent": {"x-tablename": "grandparent"},
            },
            ["Grandparent", "Parent", "Child"],
        ),
        (
            {
                "Grandparent": {"x-tablename": "grandparent"},
                "Parent": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Grandparent"},
                    ]
                },
                "Child": {
                    "allOf": [
                        {"x-inherits": True},
                        {"$ref": "#/components/schemas/Parent"},
                    ]
                },
            },
            ["Grandparent", "Parent", "Child"],
        ),
    ],
    ids=[
        "empty,                            zero",
        "single no x-tablename,            zero",
        "single x-tablename,               one",
        "$ref single x-tablename,          one",
        "multiple no x-tablename,          multiple",
        "multiple one first x-tablename,   multiple",
        "multiple one last x-tablename,    multiple",
        "multiple all x-tablename,         multiple",
        "x-inherits single child first,    multiple",
        "x-inherits single parent first,   multiple",
        "x-inherits multiple parent first, multiple",
        "x-inherits multiple child first,  multiple",
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

    model_factory.assert_has_calls(
        list(mock.call(name=name) for name in expected_calls)
    )


@pytest.mark.helper
def test_remote_ref(tmp_path, _clean_remote_schemas_store):
    """
    GIVEN remote $ref that is not normalized and file with the remote schemas
    WHEN get_remote_ref is called with the $ref
    THEN the schemas are stored under the normalized path.
    """
    # Create file
    directory = tmp_path / "base"
    directory.mkdir()
    schemas_file = directory / "original.json"
    remote_schemas_file = directory / "remote.json"
    remote_schemas_file.write_text('{"Table": {"key": "value"}}')
    # Set up remote schemas store
    helpers.ref.set_context(path=str(schemas_file))
    schemas = {"RefTable": {"$ref": "remote.json#/Table"}}
    model_factory = mock.MagicMock()

    helpers.define_all(model_factory=model_factory, schemas=schemas)
