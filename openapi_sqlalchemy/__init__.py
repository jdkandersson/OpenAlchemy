"""Map an OpenAPI schema to SQLAlchemy models."""

import functools
import typing

import typing_extensions

from . import exceptions
from . import model_factory as _model_factory
from . import types


class ModelFactory(typing_extensions.Protocol):
    """Defines interface for model factory."""

    def __call__(self, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


def init_model_factory(*, base: typing.Type, spec: types.Schema) -> ModelFactory:
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

    return cached_model_factories
