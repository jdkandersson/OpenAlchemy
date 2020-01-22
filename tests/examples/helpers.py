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


def create_model(*, filename: str, model_name: str, engine: typing.Any) -> typing.Any:
    """
    Create model for a test.

    Args:
        filename: The name of the spec file where examples/ is treated as the base
            folder.
        model_name: The name of the model to create.
        engine: The engine to connect to the database.

    Returns:
        The model.

    """
    spec = read_spec(filename=filename)
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name=model_name)
    # Initialise database
    base.metadata.create_all(engine)

    return model


def create_model_session(
    *,
    filename: str,
    model_name: str,
    engine: typing.Any,
    sessionmaker: typing.Callable[[], typing.Any],
) -> typing.Tuple[typing.Any, typing.Any]:
    """
    Create model and session for a test.

    Args:
        filename: The name of the spec file where examples/ is treated as the base
            folder.
        model_name: The name of the model to create.
        engine: The engine to connect to the database.
        sessionmaker: Session factory.

    Returns:
        The model and session as a tuple.

    """
    model = create_model(filename=filename, model_name=model_name, engine=engine)
    session = sessionmaker()

    return model, session


def create_models(
    *, filename: str, model_names: typing.Tuple[str], engine: typing.Any
) -> typing.Tuple[typing.Any, ...]:
    """
    Create model for a test.

    Args:
        filename: The name of the spec file where examples/ is treated as the base
            folder.
        model_name:s The names of the models to create.
        engine: The engine to connect to the database.

    Returns:
        The models.

    """
    spec = read_spec(filename=filename)
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    models = tuple(map(lambda name: model_factory(name=name), model_names))
    # Initialise database
    base.metadata.create_all(engine)

    return models


def create_models_session(
    *,
    filename: str,
    model_names: typing.Tuple[str],
    engine: typing.Any,
    sessionmaker: typing.Callable[[], typing.Any],
) -> typing.Tuple[typing.Any, typing.Any]:
    """
    Create model and session for a test.

    Args:
        filename: The name of the spec file where examples/ is treated as the base
            folder.
        model_names: The names of the models to create.
        engine: The engine to connect to the database.
        sessionmaker: Session factory.

    Returns:
        The models and session as a tuple.

    """
    models = create_models(filename=filename, model_names=model_names, engine=engine)
    session = sessionmaker()

    return models, session
