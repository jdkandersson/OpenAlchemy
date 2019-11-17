"""Check whether a property is readOnly."""

import typing

from open_alchemy import exceptions
from open_alchemy import types

from . import peek
from .prepare_schema import prepare_schema


def check_read_only(
    *, spec: types.Schema, schemas: typing.Optional[types.Schemas] = None
) -> bool:
    """
    Check whether the specification is a valid read only.

    Assume allOf and $ref have been resolved.

    Raise MissingArgumentError for array types when schemas is None.
    Raise MalformedSchemaError if the type is an object or array or not defined.
    Raise MalformedSchemaError if the x-backref-column is not defined.

    Args:
        spec: The spec to check.
        schemas: Used to resolve any $ref and allOf for array items.

    Returns:
        Whether the property is a read only property.

    """
    # Check for readOnly
    read_only = spec.get("readOnly")
    if read_only is None or read_only is False:
        return False

    # Check readOnly spec
    if schemas is not None:
        _check_read_only_valid(spec=spec, schemas=schemas)

    return True


def _check_read_only_valid(
    *, spec: types.Schema, array_context: bool = False, schemas: types.Schemas
) -> None:
    """
    Check that a read only specification is valid.

    Args:
        spec: The spec to check.
        array_context: Whether check is being done on an array items.
        schemas: Used to resolve any $ref.

    """
    # Check type
    try:
        type_ = peek.type_(schema=spec, schemas=schemas)
    except exceptions.TypeMissingError:
        raise exceptions.MalformedSchemaError(
            "Every readOnly property must have a type."
            if not array_context
            else "Array readOnly items must have a type."
        )

    if type_ == "array":
        if array_context:
            raise exceptions.MalformedSchemaError(
                "readOnly array items cannot be an array."
            )
        items_spec = spec.get("items")
        if items_spec is None:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must define its items."
            )
        items_spec = prepare_schema(schema=items_spec, schemas=schemas)
        _check_read_only_valid(spec=items_spec, array_context=True, schemas=schemas)
        return

    if type_ != "object":
        raise exceptions.MalformedSchemaError(
            "readOnly array item type must be an object."
            if array_context
            else "readyOnly property must be of type array."
        )

    properties = spec.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must include properties."
        )
    if not properties:
        raise exceptions.MalformedSchemaError(
            "readOnly object definition must include at least 1 property."
        )
    for property_spec in properties.values():
        property_type = peek.type_(schema=property_spec, schemas=schemas)
        if property_type in {"array", "object"}:
            raise exceptions.MalformedSchemaError(
                "readOnly object properties cannot be of type array or object."
            )
