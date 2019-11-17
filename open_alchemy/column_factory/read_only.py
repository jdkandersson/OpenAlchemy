"""
Handle readOnly property.

A readOnly property may be defined as an object or an array of object. As an object:

{
    "type": "object",
    "readOnly": True,
    "properties": {
        "property_1": {"type": "string"},
        ...
    },
}

The type of a property cannot be an object nor an array. At least 1 property must be
defined. On input, $ref and allOf is supported at the object and property level.

As an array:

{
    "type": "array",
    "readOnly": True,
    "items": {
        <object definition as above>
    },
}

The items type must be an object and all the constraints as above apply, except the
readOnly key is not required at the object level. On input, $ref and allOf is supported
at the array and item level, as well as where it is supported for the object.

The returned schema has all relevant $ref and allOf resolved. At the array level, only
the type, readOnly and items properties are preserved. At the object level, only the
type, readOnly and properties properties are preserved. At the property level, only the
type is preserved.

"""

import typing

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def handle_read_only(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Tuple[typing.List, types.Schema]:
    """
    Handle readOnly property.

    Args:
        schema: The readOnly property schema.
        schemas: Used to resolve any $ref.

    Returns:
        Empty list and transformed schema.

    """
    return [], _prepare_schema(schema=schema, schemas=schemas)


def _prepare_schema(
    *, schema: types.Schema, schemas: types.Schemas, array_context: bool = False
) -> types.Schema:
    """
    Check and transform readOnly schema to consistent format.

    Args:
        schema: The readOnly schema to operate on.
        schemas: Used to resolve any $ref.
        array_context: Whether checking is being done at the array items level. Changes
            exception messages and schema validation.

    Returns:
        The schema in a consistent format.

    """
    # Check readOnly
    if not array_context and not helpers.peek.read_only(schema=schema, schemas=schemas):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must set readOnly to True."
        )

    # Check type
    try:
        type_ = helpers.peek.type_(schema=schema, schemas=schemas)
    except exceptions.TypeMissingError:
        raise exceptions.MalformedSchemaError(
            "Every readOnly property must have a type."
            if not array_context
            else "Array readOnly items must have a type."
        )

    schema = helpers.prepare_schema(schema=schema, schemas=schemas)

    # Handle array
    if type_ == "array":
        if array_context:
            raise exceptions.MalformedSchemaError(
                "readOnly array items cannot be an array."
            )
        items_schema = schema.get("items")
        if items_schema is None:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must define its items."
            )
        object_schema = _prepare_schema(
            schema=items_schema, array_context=True, schemas=schemas
        )
        return {"type": "array", "readOnly": True, "items": object_schema}

    if type_ != "object":
        raise exceptions.MalformedSchemaError(
            "readOnly array item type must be an object."
            if array_context
            else "readyOnly property must be of type array or object."
        )

    # Handle object
    properties = schema.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must include properties."
        )
    if not properties:
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must include at least 1 property."
        )

    # Initialize schema properties to return
    properties_schema = {}

    # Process properties
    for property_name, property_schema in properties.items():
        property_type = helpers.peek.type_(schema=property_schema, schemas=schemas)
        if property_type in {"array", "object"}:
            raise exceptions.MalformedSchemaError(
                "readOnly object properties cannot be of type array nor object."
            )
        properties_schema[property_name] = {"type": property_type}

    object_schema = {"type": "object", "properties": properties_schema}
    if not array_context:
        object_schema["readOnly"] = True

    return object_schema
