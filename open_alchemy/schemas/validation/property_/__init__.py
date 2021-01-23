"""Validation for properties."""

from .... import exceptions
from .... import types as oa_types
from ....helpers import peek
from ....helpers import property_
from ....helpers import type_ as type_helper
from .. import types
from . import backref
from . import json
from . import relationship
from . import simple

Type = oa_types.PropertyType


def check_type(schemas: oa_types.Schemas, schema: oa_types.Schema) -> types.Result:
    """
    Check whether the type of a property can be calculated.

    Algorithm:
    1. check that the type is present and valid
    2. check that it is one of integer, number, string, boolean, object or array,
    3. check that x-json, if defined, is valid and
    3. check that readOnly, if defined, is valid.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        schema: The property schema to check.

    Returns:
        Whether thetype of the property can be determined.

    """
    try:
        type_ = peek.type_(schema=schema, schemas=schemas)
        if type_ not in type_helper.TYPES:
            return types.Result(False, f"{type_} is not a supported type")
        peek.json(schema=schema, schemas=schemas)
        peek.read_only(schema=schema, schemas=schemas)
        peek.write_only(schema=schema, schemas=schemas)

    except (exceptions.MalformedSchemaError, exceptions.TypeMissingError) as exc:
        return types.Result(False, f"malformed schema :: {exc}")
    except exceptions.SchemaNotFoundError as exc:
        return types.Result(False, f"reference :: {exc}")

    return types.Result(True, None)


def check(
    schemas: oa_types.Schemas,
    parent_schema: oa_types.Schema,
    property_name: str,
    property_schema: oa_types.Schema,
) -> types.Result:
    """
    Check the schema for a property.

    Args:
        schemas: All defined schemas used to resolve any $ref.
        parent_schema: The schema the property is embedded in.
        property_name: The name of the property.
        property_schema: The schema to check.

    Returns:
        Whether the property is valid.

    """
    type_result = check_type(schema=property_schema, schemas=schemas)
    if not type_result.valid:
        return type_result

    type_ = property_.calculate_type(schema=property_schema, schemas=schemas)

    if type_ == Type.BACKREF:
        return backref.check(schema=property_schema, schemas=schemas)
    if type_ == Type.SIMPLE:
        return simple.check(schema=property_schema, schemas=schemas)
    if type_ == Type.JSON:
        return json.check(schema=property_schema, schemas=schemas)
    return relationship.check(
        property_name=property_name,
        property_schema=property_schema,
        parent_schema=parent_schema,
        schemas=schemas,
    )
