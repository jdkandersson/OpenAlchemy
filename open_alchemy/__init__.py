"""Map an OpenAPI schema to SQLAlchemy models."""

import functools
import sys
import types as py_types
import typing

from sqlalchemy.ext import declarative

from open_alchemy import types as oa_types

from . import exceptions
from . import helpers as _helpers
from . import model_factory as _model_factory
from . import models_file as _models_file

models = py_types.ModuleType("models")  # pylint: disable=invalid-name
sys.modules["open_alchemy.models"] = models


def init_model_factory(
    *,
    base: typing.Type,
    spec: oa_types.Schema,
    define_all: bool = False,
    models_filename: typing.Optional[str] = None,
    spec_path: typing.Optional[str] = None,
) -> oa_types.ModelFactory:
    """
    Create factory that generates SQLAlchemy models based on OpenAPI specification.

    Args:
        base: The declarative base for the models.
        spec: The OpenAPI specification in the form of a dictionary.
        define_all: Whether to define all the models during initialization.
        models_filename: The name of the file to write the models typing information to.
        spec_path: The path the the OpenAPI specification. Mainly used to support remote
            references.

    Returns:
        A factory that returns SQLAlchemy models derived from the base based on the
        OpenAPI specification.

    """
    # Record the spec path
    if spec_path is not None:
        _helpers.ref.set_context(path=spec_path)

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

    # Intercept factory calls to make models available
    def _register_model(*, name: str) -> typing.Type:
        """Intercept calls to model factory and register model on models."""
        model = cached_model_factories(name=name)
        setattr(models, name, model)
        return model

    if define_all:
        # Write the schemas file
        if models_filename is not None:
            models_file = _models_file.ModelsFile()

            # Intercept factory calls to record the schema
            def _record_schema(*, name: str) -> typing.Type:
                """Intercept calls to model factory and record schema."""
                model = _register_model(name=name)
                models_file.add_model(
                    schema=model._schema, name=name  # pylint: disable=protected-access
                )
                return model

            _helpers.define_all(model_factory=_record_schema, schemas=schemas)

            with open(models_filename, "w") as out_file:
                out_file.write(models_file.generate_models())

            return _record_schema

        _helpers.define_all(model_factory=_register_model, schemas=schemas)

    return _register_model


BaseAndModelFactory = typing.Tuple[typing.Type, oa_types.ModelFactory]


def _init_optional_base(
    *,
    base: typing.Optional[typing.Type],
    spec: oa_types.Schema,
    define_all: bool,
    models_filename: typing.Optional[str] = None,
    spec_path: typing.Optional[str] = None,
) -> BaseAndModelFactory:
    """Wrap init_model_factory with optional base."""
    if base is None:
        base = declarative.declarative_base()
    return (
        base,
        init_model_factory(
            base=base,
            spec=spec,
            define_all=define_all,
            models_filename=models_filename,
            spec_path=spec_path,
        ),
    )


def init_json(
    spec_filename: str,
    *,
    base: typing.Optional[typing.Type] = None,
    define_all: bool = True,
    models_filename: typing.Optional[str] = None,
) -> BaseAndModelFactory:
    """
    Create SQLAlchemy models factory based on an OpenAPI specification as a JSON file.

    Args:
        spec_filename: filename of an OpenAPI spec in JSON format
        base: The declarative base for the models.
        models_filename: (optional) The path to write the models file to. If it is not
            provided, the models file is not created.

    Returns:
        A tuple (Base, model_factory), where:

        Base: a SQLAlchemy declarative base class
        model_factory: A factory that returns SQLAlchemy models derived from the
            base based on the OpenAPI specification.
        define_all: (optional) Whether to define all the models during initialization.

    """
    # Most OpenAPI specs are YAML, so, for efficiency, we only import json if we
    # need it:
    import json  # pylint: disable=import-outside-toplevel

    with open(spec_filename) as spec_file:
        spec = json.load(spec_file)

    return _init_optional_base(
        base=base,
        spec=spec,
        define_all=define_all,
        models_filename=models_filename,
        spec_path=spec_filename,
    )


def init_yaml(
    spec_filename: str,
    *,
    base: typing.Optional[typing.Type] = None,
    define_all: bool = True,
    models_filename: typing.Optional[str] = None,
) -> BaseAndModelFactory:
    """
    Create SQLAlchemy models factory based on an OpenAPI specification as a YAML file.

    Raise ImportError if pyyaml has not been installed.

    Args:
        spec_filename: filename of an OpenAPI spec in YAML format
        base: (optional) The declarative base for the models.
              If base=None, construct a new SQLAlchemy declarative base.
        define_all: (optional) Whether to define all the models during initialization.
        models_filename: (optional) The path to write the models file to. If it is not
            provided, the models file is not created.

    Returns:
        A tuple (Base, model_factory), where:

        Base: a SQLAlchemy declarative base class
        model_factory: A factory that returns SQLAlchemy models derived from the
            base based on the OpenAPI specification.
        define_all: Whether to define all the models during initialization.

    """
    try:
        import yaml  # pylint: disable=import-outside-toplevel
    except ImportError:
        raise ImportError(
            "Using init_yaml requires the pyyaml package. Try `pip install pyyaml`."
        )

    with open(spec_filename) as spec_file:
        spec = yaml.load(spec_file, Loader=yaml.SafeLoader)

    return _init_optional_base(
        base=base,
        spec=spec,
        define_all=define_all,
        models_filename=models_filename,
        spec_path=spec_filename,
    )


__all__ = ["init_model_factory", "init_json", "init_yaml"]
