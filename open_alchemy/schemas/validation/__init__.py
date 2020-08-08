"""Schema validation pre-processor."""

from ... import exceptions as _exceptions
from ... import types as _types
from .. import helpers as _helpers
from . import model
from . import property_


def process_model(schemas: _types.Schemas, schema_name, schema: _types.Schema) -> None:
    """
    Validate the model schema properties.

    Assume the schema is valid at the model level.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to validate.

    """
    properties = _helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    properties_results = map(
        lambda args: (args[0], property_.check(schemas, schema, args[0], args[1])),
        properties,
    )
    invalid_properties_result = next(
        filter(lambda args: not args[1].valid, properties_results), None
    )
    if invalid_properties_result is not None:
        name, result = invalid_properties_result
        raise _exceptions.MalformedSchemaError(
            f"{schema_name} :: {name} :: {result.reason}"
        )


def process(*, schemas: _types.Schemas) -> None:
    """
    Validate schemas.

    Args:
        schemas: The schemas to validate.

    """
    if not isinstance(schemas, dict):
        raise _exceptions.MalformedSchemaError("Schemas must be a dictionary.")

    # Check keys are strings
    any_key_not_string = any(
        filter(lambda key: not isinstance(key, str), schemas.keys())
    )
    if any_key_not_string:
        raise _exceptions.MalformedSchemaError("Schemas must have key strings.")
    # Check values are dictionaries
    any_values_not_string = any(
        filter(lambda value: not isinstance(value, dict), schemas.values())
    )
    if any_values_not_string:
        raise _exceptions.MalformedSchemaError("Schemas must have dictionary values.")

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
        process_model(schemas, name, schema)
