"""Schema validation pre-processor."""

import typing

from ... import cache
from ... import exceptions as _exceptions
from ... import types as _oa_types
from ..helpers import iterate
from . import association
from . import model
from . import property_
from . import schemas_validation
from . import spec_validation
from . import types
from . import unique_secondary
from . import unique_tablename


def _get_properties_results(
    schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> typing.Iterable[typing.Tuple[str, types.Result]]:
    """Get an iterator with properties results."""
    # Get model properties
    properties = iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    # Filter any keys that are not string
    properties = filter(lambda args: isinstance(args[0], str), properties)
    # Check properties
    return map(
        lambda args: (args[0], property_.check(schemas, schema, args[0], args[1])),
        properties,
    )


def _process_model(
    schemas: _oa_types.Schemas, schema_name: str, schema: _oa_types.Schema
) -> None:
    """
    Validate the model schema properties.

    Assume the schema is valid at the model level.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema_name: The name of the schema to validate.
        schema: The schema to validate.

    """
    properties_results = _get_properties_results(schemas, schema)
    invalid_properties_result = next(
        filter(lambda args: not args[1].valid, properties_results), None
    )
    if invalid_properties_result is not None:
        name, result = invalid_properties_result
        raise _exceptions.MalformedSchemaError(
            f"{schema_name} :: {name} :: {result.reason}"
        )


def _other_schemas_checks(*, schemas: _oa_types.Schemas) -> types.Result:
    """
    Check that at least 1 model is defined and for multiple tablename.

    Args:
        schemas: All defined schemas.

    Returns:
        Whether the schemas are valid with a reason if they are not.

    """
    one_model_result = check_one_model(schemas=schemas)
    if not one_model_result.valid:
        return one_model_result

    unique_tablename_result = unique_tablename.check(schemas=schemas)
    if not unique_tablename_result.valid:
        return unique_tablename_result

    unique_secondary_result = unique_secondary.check(schemas=schemas)
    if not unique_secondary_result.valid:
        return unique_secondary_result

    association_result = association.check(schemas=schemas)
    if not association_result.valid:
        return association_result

    return types.Result(valid=True, reason=None)


def process(
    *, schemas: _oa_types.Schemas, spec_filename: typing.Optional[str] = None
) -> None:
    """
    Validate schemas.

    Args:
        schemas: The schemas to validate.
        spec_filename: The filename of the spec, used to cache the result.

    """
    if spec_filename is not None:
        if cache.schemas_valid(spec_filename):
            return

    schemas_result = schemas_validation.check(schemas=schemas)
    if not schemas_result.valid:
        raise _exceptions.MalformedSchemaError(schemas_result.reason)

    # Check constructable schemas model
    constructables = iterate.constructable(schemas=schemas)
    model_results = map(
        lambda args: (args[0], model.check(schemas, args[1])), constructables
    )
    invalid_model_result = next(
        filter(lambda args: not args[1].valid, model_results), None
    )
    if invalid_model_result is not None:
        name, result = invalid_model_result
        raise _exceptions.MalformedSchemaError(f"{name} :: {result.reason}")

    # Check constructable schemas properties
    constructables = iterate.constructable(schemas=schemas)
    for constructable in constructables:
        name, schema = constructable
        _process_model(schemas, name, schema)

    other_results_result = _other_schemas_checks(schemas=schemas)
    if not other_results_result.valid:
        raise _exceptions.MalformedSchemaError(other_results_result.reason)

    if spec_filename is not None:
        cache.schemas_are_valid(spec_filename)


def check_one_model(*, schemas: _oa_types.Schemas) -> types.Result:
    """
    Check that there is at least 1 model in the schemas.

    Args:
        schemas: The schemas to validate.

    Returns:
        Whether the schemas contain at least 1 model.

    """
    constructables = iterate.constructable(schemas=schemas)
    if not any(constructables):
        return types.Result(
            False,
            "specification must define at least 1 schema with the x-tablename key",
        )

    return types.Result(True, None)


def _check_model_properties(
    *, schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> types.TProperties:
    """
    Check the properties of a model.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema_name: The name of the schema to validate.
        schema: The schema to validate.

    Returns:
        Whether the properties are valid.

    """
    properties_results = _get_properties_results(schemas, schema)
    properties_t_results: typing.Iterable[typing.Tuple[str, types.TProperty]] = map(
        lambda args: (args[0], {"result": types.t_result_from_result(args[1])}),
        properties_results,
    )
    return dict(properties_t_results)


def _check_model(schemas: _oa_types.Schemas, schema: _oa_types.Schema) -> types.TModel:
    """
    Check a model.

    Args:
        schema: The schema of the model to check.

    Returns:
        Whether the model and its properties are valid with a reason if it is not.

    """
    model_result = model.check(schemas, schema)
    return {
        "result": types.t_result_from_result(model_result),
        "properties": _check_model_properties(schemas=schemas, schema=schema),
    }


def check_models(*, schemas: _oa_types.Schemas) -> types.TModels:
    """
    Check the models of a schema.

    Assume the schemas is valid although any of its models may not.

    Args:
        schemas: The schemas to check.

    Returns:
        The result for each model.

    """
    constructables = iterate.constructable(schemas=schemas)
    constructables_result = map(
        lambda args: (args[0], _check_model(schemas, args[1])), constructables
    )
    return dict(constructables_result)


def check(*, spec: typing.Any) -> types.TSpec:
    """
    Check a specification.

    Args:
        spec: The specification to check.

    Returns:
        Whether the specification is valid with a reason if it is not.

    """
    # Check spec to schemas
    spec_result = spec_validation.check(spec=spec)
    if not spec_result.valid:
        return {"result": types.t_result_from_result(spec_result)}

    # Check that there is at least 1 model
    assert isinstance(spec, dict)
    components = spec.get("components")
    assert isinstance(components, dict)
    schemas = components.get("schemas")
    assert isinstance(schemas, dict)

    try:
        other_result = _other_schemas_checks(schemas=schemas)
        if not other_result.valid:
            return {"result": types.t_result_from_result(other_result)}
    except _exceptions.BaseError:
        # Something else is wrong
        pass

    return {"result": {"valid": True}, "models": check_models(schemas=schemas)}
