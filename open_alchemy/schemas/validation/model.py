"""Validate the schema of a model."""

# pylint: disable=unused-argument

from ... import exceptions
from ... import helpers as oa_helpers
from ... import types as oa_types
from .. import helpers
from . import types


def _check_basics(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check basics related to tablename, inheritance and type."""
    # Check for inheritance
    inherits = oa_helpers.schema.inherits(schema=schema, schemas=schemas)
    if inherits:
        oa_helpers.inheritance.get_parent(schema=schema, schemas=schemas)

    tablename = oa_helpers.peek.tablename(schema=schema, schemas=schemas)
    if tablename is None and not inherits:
        return types.Result(False, "every model must define x-tablename")

    type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)
    if type_ != "object":
        return types.Result(False, "models must have the object type")

    return None


def _check_properties(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.OptResult:
    """Check the properties."""
    properties = helpers.iterate.properties(
        schema=schema, schemas=schemas, stay_within_model=True
    )

    # Check there is at least a single property
    first_property = next(properties, None)
    if first_property is None:
        return types.Result(False, "models must have at least 1 property themself")

    # Check that all required values are lists
    required_values = helpers.iterate.required_values(schema=schema, schemas=schemas)
    required_value_not_list = any(
        filter(
            lambda required_value: not isinstance(required_value, list), required_values
        )
    )
    if required_value_not_list:
        return types.Result(False, "value of required must be a list")

    return None


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check that a schema is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The schema to validate.

    Returns:
        Whether the schema is valid with the reason if it is not.

    """
    try:
        basics_result = _check_basics(schema=schema, schemas=schemas)
        if basics_result is not None:
            return basics_result

        properties_result = _check_properties(schema=schema, schemas=schemas)
        if properties_result is not None:
            return properties_result

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
    except exceptions.MalformedExtensionPropertyError as exc:
        return types.Result(False, f"sextension property :: {exc}")

    return types.Result(True, None)
