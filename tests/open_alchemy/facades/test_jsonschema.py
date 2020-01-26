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
    THEN no exceptions are raised.
    """
    # Create file
    directory = tmp_path / "json"
    directory.mkdir()
    json_file = directory / "dict.json"
    json_file.write_text('{"RefSchema": {"type": "string"}}')
    schema = {"$ref": "#/RefSchema"}
    instance = "test"

    resolver = facades.jsonschema.resolver(str(json_file))
    jsonschema.validate(instance, schema, resolver=resolver)
