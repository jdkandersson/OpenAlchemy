"""Retrieve artifacts for a relationship property."""

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def _get_parent(*, schema: oa_types.Schema, schemas: oa_types.Schemas) -> str:
    """Retrieve the parent name from an object reference."""
    print(schema)
    ref = oa_helpers.peek.ref(schema=schema, schemas=schemas)
    assert ref is not None
    parent, _ = oa_helpers.ref.resolve(schema={"$ref": ref}, schemas=schemas, name="")
    return parent


def _get_many_to_one(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a many-to-one relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    return types.ManyToOneRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        schema={},
        required=None,
        parent=_get_parent(schema=schema, schemas=schemas),
        backref_property=None,
        kwargs=None,
        write_only=None,
        foreign_key="",
        foreign_key_property="",
        nullable=None,
    )


def _get_one_to_one(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a one-to-one relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    return types.OneToOneRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
        schema={},
        required=None,
        parent=_get_parent(schema=schema, schemas=schemas),
        backref_property=None,
        kwargs=None,
        write_only=None,
        foreign_key="",
        foreign_key_property="",
        nullable=None,
    )


def _get_one_to_many(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a one-to-many relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None

    return types.OneToManyRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
        schema={},
        required=None,
        parent=_get_parent(schema=items_schema, schemas=schemas),
        backref_property=None,
        kwargs=None,
        write_only=None,
        foreign_key="",
        foreign_key_property="",
    )


def _get_many_to_many(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a many-to-many relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None

    return types.ManyToManyRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
        schema={},
        required=None,
        parent=_get_parent(schema=items_schema, schemas=schemas),
        backref_property=None,
        kwargs=None,
        write_only=None,
        secondary="secondary",
    )


_GET_MAPPING = {
    oa_helpers.relationship.Type.MANY_TO_ONE: _get_many_to_one,
    oa_helpers.relationship.Type.ONE_TO_ONE: _get_one_to_one,
    oa_helpers.relationship.Type.ONE_TO_MANY: _get_one_to_many,
    oa_helpers.relationship.Type.MANY_TO_MANY: _get_many_to_many,
}


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema, required: bool
) -> types.TAnyRelationshipPropertyArtifacts:
    """
    Retrieve the artifacts for a relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.
        required: WHether the property appears in the required list.

    Returns:
        The artifacts for the property.

    """
    sub_type = oa_helpers.relationship.calculate_type(schema=schema, schemas=schemas)

    artifacts = _GET_MAPPING[sub_type](schema=schema, schemas=schemas)
    artifacts.required = required

    return artifacts
