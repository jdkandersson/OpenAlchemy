"""Validation for readOnly properties."""

from .... import exceptions
from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import helpers as validation_helpers
from .. import types
from . import simple


def _check_object(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> types.Result:
    """Check readOnly object."""
    # Check properties values and items
    properties_values_result = validation_helpers.properties.check_properties_values(
        schema=schema, schemas=schemas
    )
    if properties_values_result is not None:
        return properties_values_result
    properties_items_result = validation_helpers.properties.check_properties_items(
        schema=schema, schemas=schemas
    )
    if properties_items_result is not None:
        return properties_items_result

    # Get types of properties
    properties_items = helpers.iterate.properties_items(schema=schema, schemas=schemas)
    properties_items_type = map(
        lambda args: (args[0], oa_helpers.peek.type_(schema=args[1], schemas=schemas)),
        properties_items,
    )
    properties_items_type = filter(
        lambda args: args[1] not in simple.TYPES, properties_items_type
    )
    first_properties_items_type = next(properties_items_type, None)
    if first_properties_items_type is not None:
        name, type_ = first_properties_items_type
        return types.Result(
            False,
            f"properties :: {name} :: readOnly object propeerties do not support the "
            f"{type_} type",
        )

    return types.Result(True, None)


def _check_array(*, schema: oa_types.Schema, schemas: oa_types.Schemas) -> types.Result:
    """Check readOnly array."""
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is None:
        return types.Result(False, "readOnly array properties must define items")

    # Check items type
    items_type = oa_helpers.peek.type_(schema=items_schema, schemas=schemas)
    if items_type != "object":
        return types.Result(
            False, "items :: readOnly array items must have the object type"
        )

    # Check items
    object_result = _check_object(schema=items_schema, schemas=schemas)
    if not object_result.valid:
        return types.Result(False, f"items :: {object_result.reason}")

    return types.Result(True, None)


def check(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check the schema of a readOnly property.

    Args:
        schemas: The schemas used to resolve any $ref.
        schema: The schema of the property.

    Returns:
        A result with whether the schema is valid and a reason if it is not.

    """
    try:
        type_ = oa_helpers.peek.type_(schema=schema, schemas=schemas)

        assert type_ not in simple.TYPES

        oa_helpers.peek.description(schema=schema, schemas=schemas)

        if type_ == "object":
            return _check_object(schema=schema, schemas=schemas)

        if type_ == "array":
            return _check_array(schema=schema, schemas=schemas)

        return types.Result(False, f"{type_} type is not supported")

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")
