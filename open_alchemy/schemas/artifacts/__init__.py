"""Retrieve artifacts from the schemas."""

import dataclasses
import typing

from ... import types as _oa_types
from .. import helpers as _helpers
from .. import validation
from . import model
from . import property_
from . import types


def _get_properties_artifacts(
    schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> typing.Iterable[typing.Tuple[str, types.TAnyPropertyArtifacts]]:
    """Get an iterator with properties artifacts."""
    # Get model properties
    properties = _helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    required_set = set(_helpers.iterate.required_items(schema=schema, schemas=schemas))
    # Filter for valid properties
    valid_properties = filter(
        lambda args: validation.property_.check(
            schemas, schema, args[0], args[1]
        ).valid,
        properties,
    )
    return map(
        lambda args: (
            args[0],
            property_.get(schemas, schema, args[0], args[1], args[0] in required_set),
        ),
        valid_properties,
    )


def _get_properties(
    *, schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> types.PropertiesValue:
    """
    Get artifacts for the properties of a model.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema_name: The name of the schema to validate.
        schema: The schema to validate.

    Returns:
        The artifacts for the properties.

    """
    properties_artifacts = _get_properties_artifacts(schemas, schema)
    properties_t_artifacts: typing.Iterable[
        typing.Tuple[str, types.PropertyValue]
    ] = map(
        lambda args: (args[0], {"artifacts": args[1].to_dict()}),
        properties_artifacts,
    )
    return dict(properties_t_artifacts)


def _get_model(
    schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> types.ModelValue:
    """
    Get artifacts for a model.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema of the model to get artifacts for.

    Returns:
        The artifacts of the model.

    """
    model_artifacts = model.get(schemas, schema)
    return {
        "artifacts": model_artifacts.to_dict(),
        "properties": _get_properties(schemas=schemas, schema=schema),
    }


def get_models(*, schemas: _oa_types.Schemas) -> types.ModelsValue:
    """
    Get artifacts for the models of a schema.

    Assume the schemas is valid although any of its models may not.

    Args:
        schemas: The schemas to get artifacts for.

    Returns:
        The artifacts for each model.

    """
    constructables = _helpers.iterate.constructable(schemas=schemas)
    valid_constructables = filter(
        lambda args: validation.model.check(schemas, args[1]).valid, constructables
    )
    constructables_artifacts = map(
        lambda args: (args[0], _get_model(schemas, args[1])), valid_constructables
    )
    return dict(constructables_artifacts)


def get(*, spec: typing.Any) -> types.SpecValue:
    """
    Get artifacts for a specification.

    Args:
        spec: The specification to get artifacts from.

    Returns:
        The artifacts for the specification.

    """
    # Check spec to schemas
    spec_result = validation.spec_validation.check(spec=spec)
    if not spec_result.valid:
        return {}

    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)

    return {"models": get_models(schemas=schemas)}


def _from_schemas_get_properties_artifacts(
    stay_within_model: bool, schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> typing.Iterable[typing.Tuple[str, types.TAnyPropertyArtifacts]]:
    """Get an iterator with properties artifacts."""
    # Get model properties
    properties = _helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=stay_within_model
    )
    required_set = set(_helpers.iterate.required_items(schema=schema, schemas=schemas))
    return map(
        lambda args: (
            args[0],
            property_.get(schemas, schema, args[0], args[1], args[0] in required_set),
        ),
        properties,
    )


def _from_schemas_get_model(
    stay_within_model: bool, schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> types.ModelArtifacts:
    """
    Get artifacts for a model.

    Assume the schema is valid.

    Args:
        schema: The schema of the model to get artifacts for.
        schemas: All defined schemas used to resolve any $ref.
        stay_within_model: Whether only properties from within a model should be
            included.

    Returns:
        The artifacts of the model.

    """
    model_artifacts = model.get(schemas, schema)
    properties_artifacts = _from_schemas_get_properties_artifacts(
        stay_within_model, schemas, schema
    )
    return types.ModelArtifacts(
        tablename=model_artifacts.tablename,
        inherits=model_artifacts.inherits,
        parent=model_artifacts.parent,
        description=model_artifacts.description,
        mixins=model_artifacts.mixins,
        kwargs=model_artifacts.kwargs,
        composite_index=model_artifacts.composite_index,
        composite_unique=model_artifacts.composite_unique,
        backrefs=model_artifacts.backrefs,
        properties=list(properties_artifacts),
    )


def get_from_schemas(
    *, schemas: _oa_types.Schemas, stay_within_model: bool
) -> types.ModelsModelArtifacts:
    """
    Get the artifacts from schemas.

    Assume the schemas are valid.

    Args:
        schemas: The schemas to get artifacts from.
        stay_within_model: Whether only properties from within a model should be
            included.

    Returns:
        The artifacts for the schemas.

    """
    constructables = _helpers.iterate.constructable(schemas=schemas)
    return list(
        map(
            lambda args: (
                args[0],
                _from_schemas_get_model(stay_within_model, schemas, args[1]),
            ),
            constructables,
        )
    )
