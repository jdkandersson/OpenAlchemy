"""Set the foreign key on an existing model or add it to the schemas."""

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import helpers
from open_alchemy import types

from ...utility_base import TOptUtilityBase
from .. import column
from .. import object_ref


def set_(
    *,
    ref_model_name: str,
    logical_name: str,
    model_schema: types.Schema,
    schemas: types.Schemas,
    fk_column: str,
) -> None:
    """
    Set the foreign key on an existing model or add it to the schemas.

    For an array reference that is defined in the form of a one to many relationship,
    the referenced model requires the addition of a foreign key that would not generally
    be defined by the user. Therefore, the appropriate schema has to be calculated and
    then somehow added to the referenced model. At the time of processing, the
    referenced model may already have been constructed. This requires a check on
    open_alchemy.models for the referenced model. If it is there, it is modified by
    adding a new column to it. Otherwise, the schema of the referenced model is altered
    to include the column so that it is constructed when that model is processed.

    Raise MalformedRelationshipError of the referenced model is not found in the
    schemas.

    Args:
        ref_model_name: The name of the referenced model.
        logical_name: The logical name of the array reference property.
        model_schema: The schema which contains the one to many relationship.
        schemas: All the model schemas used to look for the referenced model and to
            resolve any $ref.
        fk_column: The name of the foreign key column to be added.

    """
    # Check that referenced model is in schemas
    ref_schema = schemas.get(ref_model_name)
    if ref_schema is None:
        raise exceptions.MalformedRelationshipError(
            f"{ref_model_name} referenced in relationship was not found in the "
            "schemas."
        )
    # Prepare schema for construction. Note any top level $ref must already be resolved.
    ref_schema = helpers.all_of.merge(schema=ref_schema, schemas=schemas)

    # Calculate foreign key artifacts
    tablename = helpers.peek.tablename(schema=model_schema, schemas={})
    fk_input_logical_name = f"{tablename}_{logical_name}"
    fk_logical_name, fk_artifacts = object_ref.foreign_key.gather_artifacts(
        model_schema=model_schema,
        logical_name=fk_input_logical_name,
        schemas=schemas,
        fk_column=fk_column,
    )

    # Check whether the foreign key has already been defined in the referenced model
    fk_required = object_ref.foreign_key.check_required(
        artifacts=fk_artifacts,
        fk_logical_name=fk_logical_name,
        model_schema=ref_schema,
        schemas=schemas,
    )
    if not fk_required:
        return

    # Handle model already constructed by altering the model on open_aclehmy.model
    ref_model: TOptUtilityBase = facades.models.get_model(name=ref_model_name)
    if ref_model is not None:
        column_inst = column.construct_column(artifacts=fk_artifacts)
        setattr(ref_model, fk_logical_name, column_inst)
        return

    # Handle model not constructed by adding the foreign key schema to the model schema
    fk_schema: types.Schema = column.calculate_schema(  # type: ignore
        artifacts=fk_artifacts, dict_ignore=True
    )
    fk_object_schema = {
        "type": "object",
        "properties": {
            fk_logical_name: {
                **fk_schema,
                "x-foreign-key": fk_artifacts.extension.foreign_key,
            }
        },
    }
    if "allOf" not in schemas[ref_model_name]:
        # Add new top level allOf
        schemas[ref_model_name] = {"allOf": [schemas[ref_model_name], fk_object_schema]}
        return
    # Append to existing allOf
    schemas[ref_model_name]["allOf"].append(fk_object_schema)
