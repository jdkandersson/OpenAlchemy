"""Helpers for example tests."""

import os
import typing

import yaml
from sqlalchemy.ext import declarative

import open_alchemy

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


def create_model_session(
    *,
    filename: str,
    model_name: str,
    engine: typing.Any,
    sessionmaker: typing.Callable[[], typing.Any]
) -> typing.Tuple[typing.Any, typing.Any]:
    """
    Create model and session for a test.

    Args:

    Returns:
        The model and session as a tuple.
    """
    spec = read_spec(filename=filename)
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name=model_name)
    # Initialise database
    base.metadata.create_all(engine)
    session = sessionmaker()

    return model, session
