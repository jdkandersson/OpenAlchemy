"""Pre-process schemas by adding any back references into the schemas."""

import functools
import itertools
import typing

from .. import exceptions
from .. import helpers as oa_helpers
from .. import types
from . import helpers


def _defines_backref(schemas: types.Schemas, schema: types.Schema) -> bool:
    """
    Check whether the property schema defines a back reference.

    The following rules are used:
    1. if there is an items key, recursively call on the items value.
    1. peek for x-backrefs on the schema and return True if found.
    3. Return False.

    Args:
        _: Placeholder for unused name argument.
        schema: The schema of the property.
        schemas: All the defined schemas.

    Returns:
        Whether the property defines a back reference.

    """
    # Handle items
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is not None:
        return _defines_backref(schema=items_schema, schemas=schemas)

    # Peek for backref
    backref = oa_helpers.peek.backref(schema=schema, schemas=schemas)
    if backref is not None:
        return True

    return False


class _CalculateSchemaReturn(typing.NamedTuple):
    """The return value of _calculate_schema."""

    ref_schema_name: str
    property_name: str
    schema: types.Schema


_CalculateSchemaReturnIter = typing.Iterable[_CalculateSchemaReturn]
_CalculateSchemaReturnGroupedIter = typing.Iterable[
    typing.Tuple[str, _CalculateSchemaReturnIter]
]


def _calculate_schema(
    schema_name: str, schemas: types.Schemas, schema: types.Schema
) -> _CalculateSchemaReturn:
    """
    Calculate the schema for a back reference.

    Args:
        schema: The schema of a property with a back reference.
        schema_name: The name of the schema that the property is on.
        schema: All the defines schemas.

    Returns:
        The name of the schema the back reference needs to be added to.

    """
    is_array: bool = False
    ref: typing.Optional[str]
    backref: typing.Optional[str]

    # Handle array
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    if items_schema is not None:
        if oa_helpers.peek.secondary(schema=items_schema, schemas=schemas) is not None:
            is_array = True

        ref = oa_helpers.peek.ref(schema=items_schema, schemas=schemas)
        backref = helpers.prefer_local.get(
            get_value=oa_helpers.peek.backref, schema=items_schema, schemas=schemas
        )
    # Handle object
    else:
        uselist: typing.Optional[bool] = helpers.prefer_local.get(
            get_value=oa_helpers.peek.uselist, schema=schema, schemas=schemas
        )
        if uselist is not False:
            is_array = True
        ref = oa_helpers.peek.ref(schema=schema, schemas=schemas)
        backref = helpers.prefer_local.get(
            get_value=oa_helpers.peek.backref, schema=schema, schemas=schemas
        )

    # Resolve name
    if ref is None:  # pragma: no cover
        # Should never get here
        raise exceptions.MalformedSchemaError("Could not find a reference")
    ref_schema_name, _ = oa_helpers.ref.resolve(
        name="", schema={"$ref": ref}, schemas=schemas
    )

    # Calculate schema
    if backref is None:  # pragma: no cover
        # Should never get here
        raise exceptions.MalformedSchemaError("Could not find a back reference")
    return_schema: types.Schema = {"type": "object", "x-de-$ref": schema_name}
    if is_array:
        return_schema = {"type": "array", "items": return_schema}

    return _CalculateSchemaReturn(ref_schema_name, backref, return_schema)


def _get_schema_backrefs(
    schemas: types.Schemas, schema_name: str, schema: types.Schema,
) -> _CalculateSchemaReturnIter:
    """
    Get the backrefs for a schema.

    Takes a constructable schema, gets all properties, filters for those that define a
    backref and retrieves the information to define a back reference.

    Args:
        schema: A constructable schema.
        schema_name: The name of the schema.
        schemas: All schemas.

    """
    # Get all the properties of the schema
    names_properties = helpers.iterate.properties(schema=schema, schemas=schemas)
    # Remove property name
    properties = map(lambda arg: arg[1], names_properties)
    # Remove properties that don't define back references
    defines_backref_schemas = functools.partial(_defines_backref, schemas)
    backref_properties = filter(defines_backref_schemas, properties)
    # Capture information for back references
    calculate_schema_schema_name_schemas = functools.partial(
        _calculate_schema, schema_name, schemas
    )
    return map(calculate_schema_schema_name_schemas, backref_properties)


def _get_backrefs(*, schemas: types.Schemas) -> _CalculateSchemaReturnIter:
    """
    Get all back reference information from the schemas.

    Takes all schemas, retrieves all constructable schemas, for each schema retrieves
    all back references and returns an iterable with all the captured back references.

    Args:
        schemas: The schemas to process.

    Returns:
        All backreference information.

    """
    # Retrieve all constructable schemas
    constructables = helpers.iterate.constructable(schemas=schemas)
    # Retrieve all backrefs
    _get_schema_backrefs_schemas = functools.partial(_get_schema_backrefs, schemas)
    backrefs_iters = map(
        lambda args: _get_schema_backrefs_schemas(*args), constructables
    )
    return itertools.chain(*backrefs_iters)


def _group_backrefs(
    *, backrefs: _CalculateSchemaReturnIter
) -> _CalculateSchemaReturnGroupedIter:
    """
    Group back references by schema name.

    Args:
        backrefs: The back references to group.

    Returns:
        The grouped back references.

    """
    sorted_backrefs = sorted(backrefs, key=lambda backref: backref.ref_schema_name)
    return itertools.groupby(sorted_backrefs, lambda backref: backref.ref_schema_name)


def _create_x_backrefs(backrefs: _CalculateSchemaReturnIter) -> types.Schema:
    """
    Convert to the schema with the x-backrefs value from backrefs.

    Args:
        backrefs: The back references to convert.

    Returns:
        The schema with the x-backrefs value.

    """
    return {
        "type": "object",
        "x-backrefs": {property_name: schema for _, property_name, schema in backrefs},
    }
