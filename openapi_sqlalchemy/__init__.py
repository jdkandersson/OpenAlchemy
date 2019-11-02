"""Map an OpenAPI schema to SQLAlchemy models."""

import functools
import sys
import types as py_types
import typing

import typing_extensions
from sqlalchemy.ext import declarative

from openapi_sqlalchemy import types as os_types

from . import exceptions
from . import model_factory as _model_factory

models = py_types.ModuleType("models")  # pylint: disable=invalid-name
sys.modules["openapi_sqlalchemy.models"] = models


class ModelFactory(typing_extensions.Protocol):
    """Defines interface for model factory."""

    def __call__(self, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


def init_model_factory(*, base: typing.Type, spec: os_types.Schema) -> ModelFactory:
    """
    Create factory that generates SQLAlchemy models based on OpenAPI specification.

    Args:
        base: The declarative base for the models.
        spec: The OpenAPI specification in the form of a dictionary.

    Returns:
        A factory that returns SQLAlchemy models derived from the base based on the
        OpenAPI specification.

    """
    # Retrieving the schema from the specification
    if "components" not in spec:
        raise exceptions.MalformedSpecificationError(
            '"components" is a required key in the specification.'
        )
    components = spec.get("components", {})
    if "schemas" not in components:
        raise exceptions.MalformedSpecificationError(
            '"schemas" is a required key in the components of the specification.'
        )
    schemas = components.get("schemas", {})

    # Binding the base and schemas
    bound_model_factories = functools.partial(
        _model_factory.model_factory, schemas=schemas, base=base
    )
    # Caching calls
    cached_model_factories = functools.lru_cache(maxsize=None)(bound_model_factories)

    # Making Base importable
    setattr(models, "Base", base)

    return cached_model_factories


BaseAndModelFactory = typing.Tuple[typing.Type, ModelFactory]


def _init_optional_base(
    *, base: typing.Optional[typing.Type], spec: os_types.Schema
) -> BaseAndModelFactory:
    """Wrap init_model_factory with optional base."""
    if base is None:
        base = declarative.declarative_base()
    return base, init_model_factory(base=base, spec=spec)


def init_json(
    spec_filename: str, *, base: typing.Optional[typing.Type] = None
) -> BaseAndModelFactory:
    """
    Create SQLAlchemy models factory based on an OpenAPI specification as a JSON file.

    Args:
        spec_filename: filename of an OpenAPI spec in JSON format
        base: The declarative base for the models.

    Returns:
        A tuple (Base, model_factory), where:

        Base: a SQLAlchemy declarative base class
        model_factory: A factory that returns SQLAlchemy models derived from the
                       base based on the OpenAPI specification.

    """
    # Most OpenAPI specs are YAML, so, for efficiency, we only import json if we
    # need it:
    import json  # pylint: disable=import-outside-toplevel

    with open(spec_filename) as spec_file:
        spec = json.load(spec_file)

    return _init_optional_base(base=base, spec=spec)


def init_yaml(
    spec_filename: str, *, base: typing.Optional[typing.Type] = None
) -> BaseAndModelFactory:
    """
    Create SQLAlchemy models factory based on an OpenAPI specification as a YAML file.

    Raise ImportError if pyyaml has not been installed.

    Args:
        spec_filename: filename of an OpenAPI spec in YAML format
        base: (optional) The declarative base for the models.
              If base=None, construct a new SQLAlchemy declarative base.

    Returns:
        A tuple (Base, model_factory), where:

        Base: a SQLAlchemy declarative base class
        model_factory: A factory that returns SQLAlchemy models derived from the
                       base based on the OpenAPI specification.

    """

    try:
        import yaml  # pylint: disable=import-outside-toplevel
    except ImportError:
        raise ImportError(
            "Using init_yaml requires the pyyaml package. Try `pip install pyyaml`."
        )

    with open(spec_filename) as spec_file:
        spec = yaml.load(spec_file, Loader=yaml.Loader)

    return _init_optional_base(base=base, spec=spec)


__all__ = ["init_model_factory", "init_json", "init_yaml"]
