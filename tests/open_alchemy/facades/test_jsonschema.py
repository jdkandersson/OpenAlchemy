"""Tests for jsonschema facade."""

import jsonschema
import pytest

from open_alchemy import facades


@pytest.mark.facade
def test_filename_to_dict(tmp_path):
    """
    GIVEN file with JSON contents
    WHEN _filename_to_dict is called with the name of the file
    THEN the dictionary contents of the file are returned.
    """
    # pylint: disable=protected-access
    # Create file
    directory = tmp_path / "json"
    directory.mkdir()
    json_file = directory / "dict.json"
    json_file.write_text('{"key": "value"}')

    returned_dict = facades.jsonschema._filename_to_dict(str(json_file))

    assert returned_dict == {"key": "value"}


@pytest.mark.facade
def test_resolver_single(tmp_path):
    """
    GIVEN single file with schema, schema that references that schema and instance of
        the schema
    WHEN resolver is created and used to validate the instance
    THEN no exceptions are raised and the referenced schema is returned as a dictionary.
    """
    # Create file
    directory = tmp_path / "json"
    directory.mkdir()
    json_file = directory / "dict.json"
    json_file.write_text('{"RefSchema": {"type": "string"}}')
    schema = {"$ref": "#/RefSchema"}
    instance = "test"

    resolver, (schema_dict,) = facades.jsonschema.resolver(str(json_file))
    jsonschema.validate(instance, schema, resolver=resolver)
    assert schema_dict == {"RefSchema": {"type": "string"}}


@pytest.mark.facade
def test_resolver_multiple(tmp_path):
    """
    GIVEN multiple files with schema, schema that references those schemas and instance
        of the schema
    WHEN resolver is created and used to validate the instance
    THEN no exceptions are raised and the referenced schemas are returned as
        dictionaries.
    """
    # Create file
    directory = tmp_path / "json"
    directory.mkdir()
    json_file1 = directory / "dict1.json"
    json_file1.write_text('{"RefSchema1": {"type": "string"}}')
    json_file2 = directory / "dict2.json"
    json_file2.write_text('{"RefSchema2": {"type": "integer"}}')
    schema = {
        "type": "object",
        "properties": {
            "key1": {"$ref": "#/RefSchema1"},
            "key2": {"$ref": "#/RefSchema2"},
        },
    }
    instance = {"key1": "value 1", "key2": 1}

    resolver, (schema1_dict, schema2_dict) = facades.jsonschema.resolver(
        str(json_file1), str(json_file2)
    )
    jsonschema.validate(instance, schema, resolver=resolver)
    assert schema1_dict == {"RefSchema1": {"type": "string"}}
    assert schema2_dict == {"RefSchema2": {"type": "integer"}}
