"""Base class providing utilities for SQLAlchemy models."""

import json
import typing

import jsonschema
import typing_extensions

from . import exceptions
from . import types


class ModelClass(typing_extensions.Protocol):
    """Defines interface for model factory."""

    _schema: types.Schema

    @classmethod
    def _get_schema(cls) -> typing.Dict:
        """Call signature to retrieve schema."""
        ...

    @classmethod
    def _get_properties(cls) -> typing.Dict:
        """Call signature to retrieve properties."""
        ...

    def __init__(  # pylint: disable=super-init-not-called
        self, kwargs: typing.Any
    ) -> None:
        """Construct."""
        ...


# ModelClass = typing.TypeVar("ModelClass", bound="UtilityBase")


class UtilityBase:
    """Base class providing utilities for SQLAlchemy models."""

    # Record of the schema used to construct the model. Myst be an object type. For all
    # columns any $ref must be resolved an allOf must be merged for all. Objects must
    # be recorded as a free-form object and have a x-de-$ref extension property with
    # the de-referenced name of the schema.
    _schema: types.Schema

    @classmethod
    def _get_schema(cls: typing.Type[ModelClass]) -> typing.Dict:
        """
        Get the schema.

        Raise ModelAttributeError if _schema is not defined.

        Returns:
            The schema.

        """
        # Checking for _schema
        if not hasattr(cls, "_schema"):
            raise exceptions.ModelAttributeError(
                "Model does not have a record of its schema. "
                "To support to_dict set the _schema class variable."
            )
        return cls._schema

    @classmethod
    def _get_properties(cls: typing.Type[ModelClass]) -> typing.Dict:
        """
        Get the properties from the schema.

        Raise ModelAttributeError if _schema is not defined.
        Raise MalformedSchemaError if the schema does not have any properties.

        Returns:
            The properties of the schema.

        """
        schema = cls._get_schema()
        # Checking that _schema has properties
        properties = schema.get("properties")
        if properties is None:
            raise exceptions.MalformedSchemaError(
                "The model schema does not have any properties."
            )
        return properties

    @classmethod
    def from_dict(cls: typing.Type[ModelClass], **kwargs: typing.Any) -> ModelClass:
        """
        Construct model instance from a dictionary.

        Raise MalformedModelDictionaryError when the dictionary does not satisfy the
        model schema.

        Args:
            kwargs: The values to construct the class with.

        Returns:
            An instance of the model constructed using the dictionary.

        """
        # Check dictionary
        schema = cls._get_schema()
        try:
            jsonschema.validate(instance=kwargs, schema=schema)
        except jsonschema.ValidationError:
            raise exceptions.MalformedModelDictionaryError(
                "The dictionary used to construct the model does not match the schema "
                "of the model. "
                f"The expected schema is {json.dumps(schema)}. "
                f"The given value is {json.dumps(kwargs)}."
            )

        return cls(**kwargs)

    def to_dict(self) -> typing.Dict:
        """
        Convert model instance to dictionary.

        Raise TypeMissingError if a property does not have a type.

        Returns:
            The dictionary representation of the model.

        """
        properties = self._get_properties()

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
