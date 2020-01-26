"""Facade for jsonschema."""

import functools
import json
import typing

import jsonschema

# Re mapping values
ValidationError = jsonschema.ValidationError
validate = jsonschema.validate  # pylint: disable=invalid-name


def _filename_to_dict(filename: str) -> typing.Dict:
    """
    Map filename for a JSON file to the loaded dictionary.

    Args:
        filename: The name of the JSON file.

    Returns:
        The contents of the file loaded as a dictionary.

    """
    with open(filename) as in_file:
        json_dict = json.loads(in_file.read())
    return json_dict


def resolver(*filenames: str) -> jsonschema.RefResolver:
    """
    Resolve references to schemas from another file.

    Args:
        filenames: The names for the files to add to the resolver.

    Returns:
        The resolver.

    """
    schema_dicts = map(_filename_to_dict, filenames)
    initial: typing.Dict = {}
    merged_schema = functools.reduce(lambda x, y: {**x, **y}, schema_dicts, initial)
    return jsonschema.RefResolver.from_schema(merged_schema)
