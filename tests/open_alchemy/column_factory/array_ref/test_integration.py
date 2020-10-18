"""Integration tests for array references."""

import pytest

from open_alchemy.column_factory import array_ref


@pytest.mark.column
def test_handle_array():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN relationship is returned pointing to the referenced schema.
    """
    schema = {"type": "array", "items": {"$ref": "#/components/schemas/RefSchema"}}
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }
    logical_name = "ref_schema"

    ([(tbl_logical_name, relationship)], return_schema) = array_ref.handle_array(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert relationship.argument == "RefSchema"
    assert relationship.backref is None
    assert relationship.secondary is None
    assert tbl_logical_name == logical_name
    assert return_schema == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }
    assert schemas == {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }


@pytest.mark.column
def test_handle_array_backref():
    """
    GIVEN schema with array referencing another schema with a back reference and schemas
    WHEN handle_array is called
    THEN relationship is returned with a back reference.
    """
    schema = {
        "type": "array",
        "items": {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "schema"},
            ]
        },
    }
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }
    logical_name = "ref_schema"

    ([(_, relationship)], _) = array_ref.handle_array(
        schema=schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert relationship.backref == ("schema", {"uselist": None})
    assert schemas == {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }
