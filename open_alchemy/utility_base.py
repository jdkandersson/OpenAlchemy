"""Base class providing utilities for SQLAlchemy models."""

import typing

from . import exceptions
from . import types


class UtilityBase:
    """Base class providing utilities for SQLAlchemy models."""

    # Record of the schema used to construct the model. Myst be an object type. For all
    # columns any $ref must be resolved an allOf must be merged for all. Objects must
    # be recorded as a free-form object and have a x-de-$ref extension property with
    # the de-referenced name of the schema.
    _schema: types.Schema

    def to_dict(self) -> typing.Dict:
        """
        Convert model instance to dictionary.

        Raise ModelAttributeError if _schema is not defined.

        Returns:
            The dictionary representation of the model.

        """
        # Checking for _schema
        if not hasattr(self, "_schema"):
            raise exceptions.ModelAttributeError(
                "Model does not have a record of its schema. "
                "To support to_dict set the _schema class variable."
            )
        # Checking that _schema has properties
        properties = self._schema.get("properties")
        if properties is None:
            raise exceptions.MalformedSchemaError(
                "The model schema does not have any properties."
            )

        # Collecting the values of the properties
        return_dict = {}
        for name, spec in properties.items():
            type_ = spec.get("type")
            if type_ is None:
                raise exceptions.TypeMissingError(
                    f"The schema for the {name} property does not have a type."
                )

            # Handle basic types
            if type_ != "object":
                return_dict[name] = getattr(self, name, None)
                continue

            # Object type
            object_value = getattr(self, name, None)
            if object_value is None:
                return_dict[name] = getattr(self, name, None)
                continue
            try:
                return_dict[name] = object_value.to_dict()
            except AttributeError:
                raise exceptions.InvalidModelInstanceError(
                    "Object property instance does not have a to_dict implementation."
                )

        return return_dict
