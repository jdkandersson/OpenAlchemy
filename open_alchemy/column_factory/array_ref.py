"""Functions relating to object references in arrays."""

import typing

import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def handle_array(
    *, spec: types.Schema, schemas: types.Schemas, logical_name: str
) -> typing.Tuple[typing.List[typing.Tuple[str, typing.Type]], types.Schema]:
    """
    Generate properties for a reference to another object through an array.

    Assume that when any allOf and $ref are resolved in the root spec the type is
    array.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.
        schema_name: The name of the schema the property belongs to.

    Returns:
        The logical name and the relationship for the referenced object.

    """
    # Resolve any allOf and $ref
    spec = helpers.prepare_schema(schema=spec, schemas=schemas)

    # Get item specification
    item_spec = spec.get("items")
    if item_spec is None:
        raise exceptions.MalformedRelationshipError(
            "An array property must include items property."
        )
    ref = item_spec.get("$ref")
    all_of = item_spec.get("allOf")

    if ref is not None:
        # Handle $ref
        ref_logical_name, ref_spec = helpers.resolve_ref(
            name=logical_name, schema=item_spec, schemas=schemas
        )
    elif all_of is not None:
        # Checking for $ref presence
        ref_count = 0
        for sub_spec in all_of:
            if sub_spec.get("$ref") is not None:
                ref_count += 1
        if ref_count != 1:
            raise exceptions.MalformedRelationshipError(
                "One to many relationships defined with allOf must have exactly one "
                "$ref in the allOf list."
            )

        # Handle all of
        for sub_spec in all_of:
            if sub_spec.get("$ref") is not None:
                ref_logical_name, ref_spec = helpers.resolve_ref(
                    name=logical_name, schema=sub_spec, schemas=schemas
                )
    else:
        raise exceptions.MalformedRelationshipError(
            "One to many relationships are defined using either $ref or allOf in the "
            "items property."
        )

    # Check referenced specification
    ref_spec = helpers.prepare_schema(schema=ref_spec, schemas=schemas)
    ref_type = ref_spec.get("type")
    if ref_type != "object":
        raise exceptions.MalformedRelationshipError(
            "One to many relationships must reference an object type " "schema."
        )
    ref_tablename = helpers.get_ext_prop(source=ref_spec, name="x-tablename")
    if ref_tablename is None:
        raise exceptions.MalformedRelationshipError(
            "One to many relationships must reference a schema with "
            "x-tablename defined."
        )

    # Construct relationship
    relationship_return = (logical_name, sqlalchemy.orm.relationship(ref_logical_name))
    # COnstruct entry for the model schema
    spec_return = {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": ref_logical_name},
    }

    return [relationship_return], spec_return
