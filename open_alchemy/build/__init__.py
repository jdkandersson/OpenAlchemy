"""Build a package with the OpenAlchemy models."""

import json
import pathlib
import typing

import jinja2

from .. import exceptions
from .. import models_file
from .. import schemas as schemas_module
from .. import types

_DIRECTORY = pathlib.Path(__file__).parent.absolute()
with open(_DIRECTORY / "setup.j2") as in_file:
    _SETUP_TEMPLATE = in_file.read()
with open(_DIRECTORY / "init_init_open_alchemy.j2") as in_file:
    _INIT_INIT_OPEN_ALCHEMY_TEMPLATE = in_file.read()


def get_schemas(*, spec: typing.Any) -> types.Schemas:
    """
    Get the schemas from the specification.

    Raises MalformedSchemaError if keys to the schemas are missing or the
    schemas are not valid.

    Args:
        spec: The spec to retrieve schemas from.

    Returns:
        The schemas after validation.

    """
    # Check to schemas
    result = schemas_module.validation.spec_validation.check(spec=spec)
    if not result.valid:
        raise exceptions.MalformedSchemaError(result.reason)

    # Check that there is at least 1 model
    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)
    one_model_result = schemas_module.validation.check_one_model(schemas=schemas)
    if not one_model_result.valid:
        raise exceptions.MalformedSchemaError(one_model_result.reason)

    # Check schemas
    schemas_module.process(schemas=schemas)

    return schemas


def generate_spec(*, schemas: types.Schemas) -> str:
    """
    Generate the spec.json file contents.

    Args:
        schemas: The schemas to generate the spec for.

    Returns:
        The JSON encoded schemas.

    """
    return json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))


def generate_setup(*, name: str, version: str) -> str:
    """
    Generate the content of the setup.py file.

    Args:
        name: The name of the package.
        version: The version of the package.

    Returns:
        The contents of the setup.py file for the models package.

    """
    template = jinja2.Template(_SETUP_TEMPLATE)

    return template.render(
        name=name,
        version=version,
    )


def generate_init_open_alchemy() -> str:
    """
    Generate the OpenAlchemy initialization component of the __init__ file.

    Returns:
        The OpenAlchemy initialization portion of the __init__ file.

    """
    template = jinja2.Template(_INIT_INIT_OPEN_ALCHEMY_TEMPLATE)

    return template.render()


def generate_init_models_file(schemas: types.Schemas) -> str:
    """
    Generate the models file component of init.

    Args:
        schemas: All defined schemas.

    Returns:
        The models file component of the schemas.

    """
    schemas_module.backref.process(schemas=schemas)
    artifacts = schemas_module.artifacts.get_from_schemas(
        schemas=schemas, stay_within_model=False
    )
    return models_file.generate(artifacts=artifacts)
