"""Check whether a property is readOnly."""

import typing

from open_alchemy import exceptions
from open_alchemy import types

from .get_ext_prop import get_ext_prop
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
    _check_read_only_valid(spec=spec, schemas=schemas)

    return True


def _check_read_only_valid(
    *,
    spec: types.Schema,
    array_context: bool = False,
    schemas: typing.Optional[types.Schemas] = None,
) -> None:
    """
    Check that a read only specification is valid.

    Args:
        spec: The spec to check.
        array_context: Whether check is being done on an array items.
        schemas: Used to resolve $ref for array items.

    """
    # Check type
    type_ = spec.get("type")
    if type_ is None:
        raise exceptions.MalformedSchemaError(
            "Every readOnly property must have a type."
            if not array_context
            else "Array readOnly items must have a type."
        )
    if type_ == "object":
        raise exceptions.MalformedSchemaError(
            "readOnly properties cannot be an object."
            if not array_context
            else "readOnly array items cannot be an object."
        )

    if type_ == "array":
        if array_context:
            raise exceptions.MalformedSchemaError(
                "readOnly array items cannot be an array."
            )
        if schemas is None:
            raise exceptions.MissingArgumentError(
                "check_read_only for arrays must be called with schemas not None."
            )
        items_spec = spec.get("items")
        if items_spec is None:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must define its items."
            )
        items_spec = prepare_schema(schema=items_spec, schemas=schemas)
        _check_read_only_valid(spec=items_spec, array_context=True)

    # Check x-backref-column
    if type_ != "array":
        backref_column = get_ext_prop(source=spec, name="x-backref-column")
        if backref_column is None:
            raise exceptions.MalformedSchemaError(
                (
                    "Every readOnly property "
                    if not array_context
                    else "Every readOnly array items "
                )
                + "must define the column of the relationship to return using "
                '"x-backref-column".'
            )
