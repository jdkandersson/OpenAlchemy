"""Schema validation pre-processor."""

import typing

from ... import exceptions as _exceptions
from ... import types as _oa_types
from .. import helpers as _helpers
from . import model
from . import property_
from . import types


def _get_properties_results(
    schemas: _oa_types.Schemas, schema: _oa_types.Schema
) -> typing.Iterable[typing.Tuple[str, types.Result]]:
    """Get an iterator with properties results."""
    properties = _helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
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


def process(*, schemas: _oa_types.Schemas) -> None:
    """
    Validate schemas.

    Args:
        schemas: The schemas to validate.

    """
    schemas_result = _check_schemas(schemas=schemas)
    if not schemas_result.valid:
        raise _exceptions.MalformedSchemaError(schemas_result.reason)

    # Check constructable schemas model
    constructables = _helpers.iterate.constructable(schemas=schemas)
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
    constructables = _helpers.iterate.constructable(schemas=schemas)
    for constructable in constructables:
        name, schema = constructable
        _process_model(schemas, name, schema)


def _check_schemas(*, schemas: _oa_types.Schemas) -> types.Result:
    """
    Validate the schemas.

    Args:
        schemas: The schemas to validate.

    Returns:
        Whether the schemas are valid.

    """
    if not isinstance(schemas, dict):
        return types.Result(False, "schemas must be a dictionary")

    # Check keys are strings
    first_key_not_string = next(
        filter(lambda key: not isinstance(key, str), schemas.keys()), None,
    )
    if first_key_not_string is not None:
        return types.Result(
            False, f"schemas keys must be strings, {first_key_not_string} is not"
        )

    # Check values are dictionaries
    first_item_not_dict_value = next(
        filter(lambda args: not isinstance(args[1], dict), schemas.items()), None
    )
    if first_item_not_dict_value is not None:
        key, _ = first_item_not_dict_value
        return types.Result(False, f"the value of {key} must be a dictionary")

    # Check there is at least 1 constructable schema
    constructables = _helpers.iterate.constructable(schemas=schemas)
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
    if not model_result.valid:
        return {"result": types.t_result_from_result(model_result)}

    return {
        "result": {"valid": True},
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
    constructables = _helpers.iterate.constructable(schemas=schemas)
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
    if not isinstance(spec, dict):
        return {
            "result": {"valid": False, "reason": "specification must be a dictionary"}
        }

    # Check components
    components = spec.get("components")
    if components is None:
        return {
            "result": {"valid": False, "reason": "specification must define components"}
        }
    if not isinstance(components, dict):
        return {
            "result": {
                "valid": False,
                "reason": "components value must be a dictionary",
            }
        }

    # Check schemas
    schemas = components.get("schemas")
    if schemas is None:
        return {
            "result": {"valid": False, "reason": "specification must define schemas"}
        }
    schemas_result = _check_schemas(schemas=schemas)
    if not schemas_result.valid:
        return {"result": types.t_result_from_result(schemas_result)}

    return {"result": {"valid": True}, "models": check_models(schemas=schemas)}
