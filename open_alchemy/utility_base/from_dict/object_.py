"""Convert object dictionary to column value."""

from ... import exceptions
from ... import facades
from ... import helpers
from ... import types as oa_types
from .. import types


def convert(
    value: types.TObjectDict, *, schema: oa_types.Schema
) -> types.TOptObjectCol:
    """
    Convert dictionary value to model instance.

    Raises InvalidInstanceError of the value is not a dictionary.

    Args:
        value: The value to convert.
        schema: The schema for the value.

    Returns:
        The converted value.

    """
    ref_model_name = helpers.ext_prop.get(source=schema, name="x-de-$ref")
    if ref_model_name is None:
        raise exceptions.MalformedSchemaError(
            "To construct object parameters the schema for the property must "
            "include the x-de-$ref extension property with the name of the "
            "model to construct for the property."
        )
    if not isinstance(value, dict):
        raise exceptions.InvalidInstanceError(
            "The value for an object parameter must be a dictionary."
        )
    ref_model = facades.models.get_model(name=ref_model_name)
    if ref_model is None:
        raise exceptions.SchemaNotFoundError(
            f"The referenced model {ref_model} was not found in the models."
        )
    return ref_model.from_dict(**value)
