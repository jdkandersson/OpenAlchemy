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
    Map filename for a JSON file to the de-serialized dictionary.

    Args:
        filename: The name of the JSON file.

    Returns:
        The de-serialized contents of the file as a dictionary.

    """
    with open(filename) as in_file:
        json_dict = json.loads(in_file.read())
    return json_dict


def resolver(
    *filenames: str,
) -> typing.Tuple[
    jsonschema.RefResolver, typing.Tuple[typing.Dict[str, typing.Any], ...]
]:
    """
    Create resolver for references to schemas in another file.

    Args:
        filenames: The names for the files to add to the resolver.

    Returns:
        The resolver and the underlying schemas as a dictionary.

    """
    schema_dicts = tuple(map(_filename_to_dict, filenames))
    initial: typing.Dict[str, typing.Any] = {}
    merged_schema = functools.reduce(lambda x, y: {**x, **y}, schema_dicts, initial)
    return jsonschema.RefResolver.from_schema(merged_schema), schema_dicts
