"""Map an OpenAPI schema to SQLAlchemy models."""

import functools
import sys
import types as py_types
import typing

from sqlalchemy.ext import declarative

from open_alchemy import types as oa_types

from . import build as _build_module
from . import exceptions
from . import helpers as _helpers
from . import model_factory as _model_factory
from . import models_file as _models_file
from . import schemas as _schemas_module
from .build import PackageFormat

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

    # Pre-processing schemas
    _schemas_module.process(schemas=schemas)

    # Binding the base and schemas
    bound_model_factories = functools.partial(
        _model_factory.model_factory, schemas=schemas, get_base=_get_base
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

    if models_filename is not None:
        schemas_artifacts = _schemas_module.artifacts.get_from_schemas(
            schemas=schemas, stay_within_model=False
        )
        models_file_contents = _models_file.generate(artifacts=schemas_artifacts)
        with open(models_filename, "w") as out_file:
            out_file.write(models_file_contents)

    if define_all:
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

    """
    try:
        import yaml  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise ImportError(
            "Using init_yaml requires the pyyaml package. Try `pip install pyyaml`."
        ) from exc

    with open(spec_filename) as spec_file:
        spec = yaml.load(spec_file, Loader=yaml.SafeLoader)

    return _init_optional_base(
        base=base,
        spec=spec,
        define_all=define_all,
        models_filename=models_filename,
        spec_path=spec_filename,
    )


def _get_base(*, name: str, schemas: oa_types.Schemas) -> typing.Type:
    """
    Retrieve the base class of a schema considering inheritance.

    If x-inherits is True, retrieve the parent. If it is a string, verify that the
    parent is valid. In either case, the model for that schema is used as the base
    instead of the usual base.
    If x-inherits is not present or False, return the usual base.

    Raise InheritanceConstructionOrderError if the parent of the schema has not been
    constructed when attempting to construct the child.

    Args:
        name: The name of the schema to determine the base for.
        schemas: All the schemas.

    Returns:
        The base of the model. Either the usual base or the model parent in the case of
        inheritance.

    """
    schema = schemas.get(name)
    if schema is None:
        raise exceptions.SchemaNotFoundError(f"Could not fund schema {name}.")

    if _helpers.schema.inherits(schema=schema, schemas=schemas):
        parent = _helpers.inheritance.retrieve_parent(schema=schema, schemas=schemas)
        try:
            return getattr(models, parent)
        except AttributeError as exc:
            raise exceptions.InheritanceError(
                "Any parents of a schema must be constructed before the schema can be "
                "constructed."
            ) from exc
    return getattr(models, "Base")


def build_json(
    spec_filename: str,
    package_name: str,
    dist_path: str,
    format_: PackageFormat = PackageFormat.NONE,
) -> None:
    """
    Create an OpenAlchemy distribution package with the SQLAlchemy models.

    The package can be uploaded to, for example, PyPI or a private repository for
    distribution.

    The formats can be combined with the bitwise operator or (``|``), for
    instance, building both sdist and wheel packages can be specified like that:

    .. code-block: python

        format_ = PackageFormat.SDIST|PackageFormat.WHEEL

    Args:
        spec_filename: filename of an OpenAPI spec in JSON format
        package_name: The name of the package.
        dist_path: The directory to output the package to.
        format_: (optional) The format(s) of the archive(s) to build.

    """
    # Most OpenAPI specs are YAML, so, for efficiency, we only import json if we
    # need it:
    import json  # pylint: disable=import-outside-toplevel

    with open(spec_filename) as spec_file:
        spec = json.load(spec_file)

    return _build_module.execute(
        spec=spec, name=package_name, path=dist_path, format_=format_
    )


def build_yaml(
    spec_filename: str,
    package_name: str,
    dist_path: str,
    format_: PackageFormat = PackageFormat.NONE,
) -> None:
    """
    Create an OpenAlchemy distribution package with the SQLAlchemy models.

    The package can be uploaded to, for example, PyPI or a private repository for
    distribution.

    The formats can be combined with the bitwise operator "or" (``|``), for
    instance, building both sdist and wheel packages can be specified like that:

    .. code-block:: python

        format_=PackageFormat.SDIST|PackageFormat.WHEEL

    Args:
        spec_filename: filename of an OpenAPI spec in YAML format
        package_name: The name of the package.
        dist_path: The directory to output the package to.
        format_: (optional) The format(s) of the archive(s) to build.

    """
    try:
        import yaml  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise ImportError(
            "Using init_yaml requires the pyyaml package. Try `pip install pyyaml`."
        ) from exc

    with open(spec_filename) as spec_file:
        spec = yaml.load(spec_file, Loader=yaml.SafeLoader)

    return _build_module.execute(
        spec=spec, name=package_name, path=dist_path, format_=format_
    )


__all__ = [
    "init_model_factory",
    "init_json",
    "init_yaml",
    "build_json",
    "build_yaml",
    "PackageFormat",
]
