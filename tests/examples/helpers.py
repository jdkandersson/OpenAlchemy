"""Helpers for example tests."""

import os
import typing

import yaml

_DIRECTORY = os.path.dirname(__file__)


def read_spec(*, filename: str) -> typing.Dict:
    """
    Read the spec from a file.

    Args:
        filename: The name of the spec file where examples/ is treated as the base
            folder.

    Returns:
        The spec in the file.

    """
    file_path = os.path.join(_DIRECTORY, "../../examples", filename)
    with open(file_path) as in_file:
        spec = yaml.safe_load(in_file)
    return spec
