"""Retrieve artifacts from the schemas."""

import typing

from ... import types as _oa_types
from .. import helpers as _helpers
from .. import validation
from . import model
from . import types


def _get_model(schemas: _oa_types.Schemas, schema: _oa_types.Schema) -> types.TModel:
    """
    Check a model.

    Args:
        schema: The schema of the model to get.

    Returns:
        Whether the model and its properties are valid with a reason if it is not.

    """
    model_artifacts = model.get(schemas, schema)
    return {
        "artifacts": model_artifacts.to_dict(),
    }


def get_models(*, schemas: _oa_types.Schemas) -> types.TModels:
    """
    Check the models of a schema.

    Assume the schemas is valid although any of its models may not.

    Args:
        schemas: The schemas to get.

    Returns:
        The result for each model.

    """
    constructables = _helpers.iterate.constructable(schemas=schemas)
    valid_constructables = filter(
        lambda args: validation.model.check(schemas, args[1]).valid, constructables
    )
    constructables_result = map(
        lambda args: (args[0], _get_model(schemas, args[1])), valid_constructables
    )
    return dict(constructables_result)


def get(*, spec: typing.Any) -> types.TSpec:
    """
    Check a specification.

    Args:
        spec: The specification to get.

    Returns:
        Whether the specification is valid with a reason if it is not.

    """
    # Check spec to schemas
    spec_result = validation.spec_validation.check(spec=spec)
    if not spec_result.valid:
        return {}

    # Check that there is at least 1 model
    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)

    return {"models": get_models(schemas=schemas)}
