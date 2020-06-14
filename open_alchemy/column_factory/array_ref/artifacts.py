"""Gather artifacts for array reference constructing."""

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

from .. import object_ref


def gather(
    *, schema: types.Schema, schemas: types.Schemas, logical_name: str
) -> types.ObjectArtifacts:
    """
    Gather artifacts for constructing a reference to another model from within an array.

    Args:
        schema: The schema of the array reference.
        schemas: All the model schemas used to resolve any $ref within the array
            reference schema.
        logical_name: The name of thearray reference within its parent schema.

    Returns:
        The artifacts required to construct the array reference.

    """
    # Resolve any allOf and $ref
    schema = helpers.schema.prepare(schema=schema, schemas=schemas)

    # Get item schema
    item_schema = schema.get("items")
    if item_schema is None:
        raise exceptions.MalformedRelationshipError(
            "An array property must include items property."
        )

    # Retrieve artifacts for the object reference within the array
    artifacts = object_ref.artifacts.gather(
        schema=item_schema, logical_name=logical_name, schemas=schemas
    )

    # Check for uselist
    if (
        artifacts.relationship.back_reference is not None
        and artifacts.relationship.back_reference.uselist is not None
    ):
        raise exceptions.MalformedRelationshipError(
            "x-uselist is not supported for one to many nor many to many relationships."
        )
    # Check for nullable
    if artifacts.nullable is not None:
        raise exceptions.MalformedRelationshipError(
            "nullable is not supported for one to many nor many to many relationships."
        )

    # Check referenced specification
    ref_schema = helpers.schema.prepare(schema=artifacts.spec, schemas=schemas)
    ref_tablename = helpers.ext_prop.get(source=ref_schema, name="x-tablename")
    if ref_tablename is None:
        raise exceptions.MalformedRelationshipError(
            "One to many relationships must reference a schema with "
            "x-tablename defined."
        )

    # Add description
    try:
        description = helpers.peek.description(schema=schema, schemas={})
    except exceptions.MalformedSchemaError as exc:
        raise exceptions.MalformedRelationshipError(str(exc))
    if description is not None:
        artifacts.description = description

    return artifacts
