"""Functions for object reference artifacts."""

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def gather(
    *, spec: types.Schema, logical_name: str, schemas: types.Schemas
) -> types.ObjectArtifacts:
    """
    Collect artifacts from a specification for constructing an object reference.

    Get the prepared specification, reference logical name, back reference and foreign
    key column name from a raw object specification.

    Raise MalformedRelationshipError if neither $ref nor $allOf is found.
    Raise MalformedRelationshipError if uselist is defined but backref is not.
    Raise MalformedRelationshipError if multiple $ref, x-backref, x-secondary,
    x-foreign-key-column or x-uselist are found.

    Args:
        spec: The schema for the column.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The prepared specification, reference logical name, back reference and foreign
        key column.

    """
    # Default backref
    backref = None
    # Default uselist
    uselist = None
    # Default secondary
    secondary = None
    # Initial foreign key column
    fk_column = None

    # Checking for $ref and allOf
    ref = spec.get("$ref")
    all_of = spec.get("allOf")

    if ref is not None:
        # Handle $ref
        ref_logical_name, spec = helpers.resolve_ref(
            name=logical_name, schema=spec, schemas=schemas
        )
    elif all_of is not None:
        # Checking for $ref, and x-backref and x-foreign-key-column counts
        _check_all_of(all_of_spec=all_of)

        # Handle allOf
        for sub_spec in all_of:
            backref = helpers.get_ext_prop(
                source=sub_spec, name="x-backref", default=backref
            )
            uselist = helpers.get_ext_prop(
                source=sub_spec, name="x-uselist", default=uselist
            )
            secondary = helpers.get_ext_prop(
                source=sub_spec, name="x-secondary", default=secondary
            )
            fk_column = helpers.get_ext_prop(
                source=sub_spec, name="x-foreign-key-column", default=fk_column
            )
            if sub_spec.get("$ref") is not None:
                ref_logical_name, spec = helpers.resolve_ref(
                    name=logical_name, schema=sub_spec, schemas=schemas
                )
    else:
        raise exceptions.MalformedRelationshipError(
            "Relationships are defined using either $ref or allOf."
        )

    # Resolving allOf
    spec = helpers.merge_all_of(schema=spec, schemas=schemas)

    # If backref has not been found look in referenced schema
    if backref is None:
        backref = helpers.get_ext_prop(source=spec, name="x-backref")
    # If uselist has not been found look in referenced schema
    if uselist is None:
        uselist = helpers.get_ext_prop(source=spec, name="x-uselist")
    # If secondary has not been found look in referenced schema
    if secondary is None:
        secondary = helpers.get_ext_prop(source=spec, name="x-secondary")
    # If foreign key column has not been found look in referenced schema
    if fk_column is None:
        fk_column = helpers.get_ext_prop(source=spec, name="x-foreign-key-column")
    # If foreign key column is still None, default to id
    if fk_column is None:
        fk_column = "id"

    # Check if uselist is defined and backref is not
    if uselist is not None and backref is None:
        raise exceptions.MalformedRelationshipError(
            "Relationships with x-uselist defined must also define x-backref."
        )

    back_reference_artifacts = None
    if backref is not None:
        back_reference_artifacts = types.BackReferenceArtifacts(
            property_name=backref, uselist=uselist
        )
    relationship_artifacts = types.RelationshipArtifacts(
        model_name=ref_logical_name,
        back_reference=back_reference_artifacts,
        secondary=secondary,
    )
    return types.ObjectArtifacts(spec, fk_column, relationship_artifacts)


def _check_all_of(*, all_of_spec: types.AllOfSpec) -> None:
    """
    Check format of allOf for an object reference.

    Raise MalformedRelationshipError if the allOf schema is not as expected.

    Args:
        all_of_spec: The allOf specification to check.

    """
    # Checking for $ref and x-backref counts
    ref_count = 0
    backref_count = 0
    fk_column_count = 0
    uselist_count = 0
    secondary_count = 0
    for sub_spec in all_of_spec:
        if sub_spec.get("$ref") is not None:
            ref_count += 1
        if sub_spec.get("x-backref") is not None:
            backref_count += 1
        if sub_spec.get("x-foreign-key-column") is not None:
            fk_column_count += 1
        if sub_spec.get("x-uselist") is not None:
            uselist_count += 1
        if sub_spec.get("x-secondary") is not None:
            secondary_count += 1
    if ref_count != 1:
        raise exceptions.MalformedRelationshipError(
            "Relationships defined with allOf must have exactly one $ref in the allOf "
            "list."
        )
    if backref_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Relationships may have at most 1 x-backref defined."
        )
    if fk_column_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Relationships may have at most 1 x-foreign-key-column defined."
        )
    if uselist_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Relationships may have at most 1 x-uselist defined."
        )
    if secondary_count > 1:
        raise exceptions.MalformedRelationshipError(
            "Relationships may have at most 1 x-secondary defined."
        )
