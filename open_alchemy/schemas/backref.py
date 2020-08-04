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
        schemas: All the defined schemas.
        schema: The schema of the property.

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


class _BackrefArtifacts(typing.NamedTuple):
    """The return value of _calculate_schema."""

    ref_schema_name: str
    property_name: str
    schema: types.Schema


_BackrefArtifactsIter = typing.Iterable[_BackrefArtifacts]
_BackrefArtifactsGroupedIter = typing.Iterable[typing.Tuple[str, _BackrefArtifactsIter]]
_BackrefSchemaIter = typing.Iterable[typing.Tuple[str, types.Schema]]


def _calculate_artifacts(
    schema_name: str, schemas: types.Schemas, schema: types.Schema
) -> _BackrefArtifacts:
    """
    Calculate the artifacts for the schema for a back reference.

    Args:
        schema_name: The name of the schema that the property is on.
        schema: All the defines schemas.
        schema: The schema of a property with a back reference.

    Returns:
        The name of the schema that is being referenced, the name of the property to be
        added and the schema for the back reference.

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
        backref = oa_helpers.peek.prefer_local(
            get_value=oa_helpers.peek.backref, schema=items_schema, schemas=schemas
        )
    # Handle object
    else:
        uselist: typing.Optional[bool] = oa_helpers.peek.prefer_local(
            get_value=oa_helpers.peek.uselist, schema=schema, schemas=schemas
        )
        if uselist is not False:
            is_array = True
        ref = oa_helpers.peek.ref(schema=schema, schemas=schemas)
        backref = oa_helpers.peek.prefer_local(
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

    return _BackrefArtifacts(ref_schema_name, backref, return_schema)


def _get_schema_backrefs(
    schemas: types.Schemas, schema_name: str, schema: types.Schema,
) -> _BackrefArtifactsIter:
    """
    Get the backrefs for a schema.

    Takes a constructable schema, gets all properties, filters for those that define a
    backref and retrieves the information to define a back reference.

    Args:
        schemas: All schemas.
        schema_name: The name of the schema.
        schema: A constructable schema.

    Returns:
        An iterable with all back references for the schema.

    """
    # Get all the properties of the schema
    names_properties = helpers.iterate.property_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    # Remove property name
    properties = map(lambda arg: arg[1], names_properties)
    # Remove properties that don't define back references
    defines_backref_schemas = functools.partial(_defines_backref, schemas)
    backref_properties = filter(defines_backref_schemas, properties)
    # Capture information for back references
    calculate_artifacts_schema_name_schemas = functools.partial(
        _calculate_artifacts, schema_name, schemas
    )
    return map(calculate_artifacts_schema_name_schemas, backref_properties)


def _get_backrefs(*, schemas: types.Schemas) -> _BackrefArtifactsIter:
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
    # Unpack nested iterators
    return itertools.chain(*backrefs_iters)


def _group_backrefs(*, backrefs: _BackrefArtifactsIter) -> _BackrefArtifactsGroupedIter:
    """
    Group back references by schema name.

    Args:
        backrefs: The back references to group.

    Returns:
        The grouped back references.

    """
    sorted_backrefs = sorted(backrefs, key=lambda backref: backref.ref_schema_name)
    return itertools.groupby(sorted_backrefs, lambda backref: backref.ref_schema_name)


def _backrefs_to_schema(backrefs: _BackrefArtifactsIter) -> types.Schema:
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


def _grouped_backrefs_to_schemas(
    *, grouped_backrefs: _BackrefArtifactsGroupedIter
) -> _BackrefSchemaIter:
    """
    Convert grouped backreferences to schema names and backreference schemas.

    Args:
        grouped_backrefs: The grouped back references.

    Returns:
        The schema names and backref schemas.

    """
    return map(lambda args: (args[0], _backrefs_to_schema(args[1])), grouped_backrefs)


def process(*, schemas: types.Schemas):
    """
    Pre-process the schemas to add backreferences as required.

    Args:
        schemas: The schemas to process.

    """
    # Retrieve back references
    backrefs = _get_backrefs(schemas=schemas)
    # Group by schema name
    grouped_backrefs = _group_backrefs(backrefs=backrefs)
    # Map to a schema for each grouped backreference
    backref_schemas = _grouped_backrefs_to_schemas(grouped_backrefs=grouped_backrefs)
    # Convert to list to resolve iterator
    backref_schemas = list(backref_schemas)
    # Add backreferences to schemas
    for name, backref_schema in backref_schemas:
        schemas[name] = {"allOf": [schemas[name], backref_schema]}
