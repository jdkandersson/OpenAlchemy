"""Pre-process schemas by adding any back references into the schemas."""

import functools
import typing

from .. import helpers as oa_helpers
from .. import types
from . import helpers


class TArtifacts(helpers.process.TArtifacts):
    """The return value of _calculate_schema."""

    property_schema: types.Schema


def _calculate_artifacts(
    schema_name: str, schemas: types.Schemas, schema: types.Schema
) -> TArtifacts:
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
    assert ref is not None
    ref_schema_name, _ = oa_helpers.ref.get_ref(ref=ref, schemas=schemas)

    # Calculate schema
    assert backref is not None
    return_schema: types.Schema = {"type": "object", "x-de-$ref": schema_name}
    if is_array:
        return_schema = {"type": "array", "items": return_schema}

    return TArtifacts(ref_schema_name, backref, return_schema)


def _get_schema_backrefs(
    schemas: types.Schemas,
    schema_name: str,
    schema: types.Schema,
) -> helpers.process.TArtifactsIter:
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
    names_properties = helpers.iterate.properties_items(
        schema=schema, schemas=schemas, stay_within_model=True
    )
    # Remove property name
    properties = map(lambda arg: arg[1], names_properties)
    # Remove properties that don't define back references
    defines_backref_schemas = functools.partial(helpers.backref.defined, schemas)
    backref_properties = filter(defines_backref_schemas, properties)
    # Capture information for back references
    calculate_artifacts_schema_name_schemas = functools.partial(
        _calculate_artifacts, schema_name, schemas
    )
    return map(calculate_artifacts_schema_name_schemas, backref_properties)


def _backrefs_to_schema(backrefs: helpers.process.TArtifactsIter) -> types.Schema:
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


def process(*, schemas: types.Schemas):
    """
    Pre-process the schemas to add back references as required.

    Args:
        schemas: The schemas to process.

    """
    # Retrieve back references
    backrefs = helpers.process.get_artifacts(
        schemas=schemas, get_schema_artifacts=_get_schema_backrefs
    )
    # Map to a schema for each grouped back references
    backref_schemas = helpers.process.calculate_outputs(
        artifacts=backrefs, calculate_output=_backrefs_to_schema
    )
    # Convert to list to resolve iterator
    backref_schema_list = list(backref_schemas)
    # Add backreferences to schemas
    for name, backref_schema in backref_schema_list:
        schemas[name] = {"allOf": [schemas[name], backref_schema]}
