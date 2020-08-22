"""Base class providing utilities for SQLAlchemy models."""

import functools
import json
import typing

from .. import exceptions
from .. import facades
from .. import helpers
from .. import types as oa_types
from . import from_dict
from . import repr_
from . import to_dict

TUtilityBase = typing.TypeVar("TUtilityBase", bound="UtilityBase")
TOptUtilityBase = typing.Optional[TUtilityBase]


class UtilityBase:
    """Base class providing utilities for SQLAlchemy models."""

    # Record of the schema used to construct the model. Must be an object type. For all
    # columns any $ref must be resolved an allOf must be merged for all. Objects must
    # be recorded as a free-form object and have a x-de-$ref extension property with
    # the de-referenced name of the schema.
    _schema: typing.ClassVar[oa_types.Schema]

    def __init__(self, **kwargs: typing.Any) -> None:
        """Construct."""
        raise NotImplementedError

    @classmethod
    def _get_schema(cls) -> oa_types.Schema:
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
    def get_properties(cls) -> oa_types.Schema:
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
                "The model schema does not have any properties.", schema=schema
            )
        return properties

    @staticmethod
    def _get_parent(*, schema: oa_types.Schema) -> typing.Type[TUtilityBase]:
        """Get the parent model of a model."""
        parent_name = helpers.ext_prop.get(source=schema, name="x-inherits")
        if parent_name is None or not isinstance(parent_name, str):
            raise exceptions.MalformedSchemaError(
                "To construct a model that inherits x-inherits must be present and a "
                "string.",
                schema=schema,
                x_inherits=parent_name,
                x_inherits_type=type(parent_name),
            )
        # Try to get model
        parent: TOptUtilityBase = facades.models.get_model(name=parent_name)
        if parent is None:
            raise exceptions.SchemaNotFoundError(
                "The parent model was not found on open_alchemy.models.",
                schema=schema,
                parent_model_name=parent_name,
            )
        return parent

    @classmethod
    def construct_from_dict_init(
        cls: typing.Type[TUtilityBase], **kwargs: typing.Any
    ) -> typing.Dict[str, typing.Any]:
        """Construct the dictionary passed to model construction."""
        # Check dictionary
        schema = cls._get_schema()
        try:
            facades.jsonschema.validate(instance=kwargs, schema=schema)
        except facades.jsonschema.ValidationError as exc:
            raise exceptions.MalformedModelDictionaryError(
                "The dictionary passed to from_dict is not a valid instance of the "
                "model schema.",
                schema=schema,
                kwargs=kwargs,
            ) from exc

        # Assemble dictionary for construction
        properties = cls.get_properties()
        model_dict: typing.Dict[str, typing.Any] = {}
        for name, value in kwargs.items():
            # Get the specification and type of the property
            property_schema = properties.get(name)
            if property_schema is None:
                raise exceptions.MalformedModelDictionaryError(
                    "A parameter was passed in that is not a property in the model "
                    "schema.",
                    parameter_name=name,
                    schema=schema,
                )

            # Convert to column value
            try:
                model_dict[name] = from_dict.convert(
                    value=value, schema=property_schema
                )
            except exceptions.BaseError as exc:
                exc.schema = schema  # type: ignore
                exc.property_schema = property_schema  # type: ignore
                exc.property_name = name  # type: ignore
                exc.property_value = value  # type: ignore
                raise

        return model_dict

    @classmethod
    def from_dict(cls: typing.Type[TUtilityBase], **kwargs: typing.Any) -> TUtilityBase:
        """
        Construct model instance from a dictionary.

        Raise MalformedModelDictionaryError when the dictionary does not satisfy the
        model schema.

        Args:
            kwargs: The values to construct the class with.

        Returns:
            An instance of the model constructed using the dictionary.

        """
        schema = cls._get_schema()
        # Handle model that inherits
        if helpers.schema.inherits(schema=schema, schemas={}):
            # Retrieve parent model
            parent: typing.Type[UtilityBase] = cls._get_parent(schema=schema)

            # Construct parent initialization dictionary
            # Get properties for schema
            properties = cls.get_properties()
            # Pass kwargs that don't belong to the current model to the parent
            parent_kwargs = {
                key: value for key, value in kwargs.items() if key not in properties
            }
            parent_init_dict = parent.construct_from_dict_init(**parent_kwargs)

            # COnstruct child (the current model) initialization dictionary
            child_kwargs = {
                key: value for key, value in kwargs.items() if key in properties
            }
            init_dict = {
                **parent_init_dict,
                **cls.construct_from_dict_init(**child_kwargs),
            }
        else:
            init_dict = cls.construct_from_dict_init(**kwargs)

        return cls(**init_dict)

    @classmethod
    def from_str(cls: typing.Type[TUtilityBase], value: str) -> TUtilityBase:
        """
        Construct model instance from a JSON string.

        Raise MalformedModelDictionaryError when the value is not a string or the string
        is not valid JSON.

        Args:
            kwargs: The values to construct the class with.

        Returns:
            An instance of the model constructed using the dictionary.

        """
        if not isinstance(value, str):
            raise exceptions.MalformedModelDictionaryError(
                "The value is not of type string.", value=value, value_type=type(value)
            )
        try:
            dict_value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise exceptions.MalformedModelDictionaryError(
                "The string value is not valid JSON.", value=value
            ) from exc
        if not isinstance(dict_value, dict):
            raise exceptions.MalformedModelDictionaryError(
                "The string value is not a Python dictionary.",
                value=value,
                value_type=type(value),
            )
        return cls.from_dict(**dict_value)

    @classmethod
    def instance_to_dict(cls, instance: TUtilityBase) -> typing.Dict[str, typing.Any]:
        """Convert instance of the model to a dictionary."""
        schema = cls._get_schema()
        properties = cls.get_properties()

        # Collecting the values of the properties
        return_dict: typing.Dict[str, typing.Any] = {}
        for name, property_schema in properties.items():
            # Handle for writeOnly
            if helpers.peek.write_only(schema=property_schema, schemas={}):
                continue

            value = getattr(instance, name, None)

            # Handle none value
            if value is None:
                return_none = to_dict.return_none(schema=schema, property_name=name)
                if return_none is True:
                    return_dict[name] = None
                # Don't consider for coverage due to coverage bug
                continue  # pragma: no cover

            try:
                return_dict[name] = to_dict.convert(schema=property_schema, value=value)
            except exceptions.BaseError as exc:
                exc.schema = schema  # type: ignore
                exc.property_schema = property_schema  # type: ignore
                exc.property_name = name  # type: ignore
                exc.property_value = value  # type: ignore
                raise

        return return_dict

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Convert model instance to dictionary.

        Returns:
            The dictionary representation of the model.

        """
        schema = self._get_schema()
        if helpers.schema.inherits(schema=schema, schemas={}):
            # Retrieve parent model and convert to dict
            parent: typing.Type[UtilityBase] = self._get_parent(schema=schema)
            parent_dict = parent.instance_to_dict(self)
            return {**parent_dict, **self.instance_to_dict(self)}

        return self.instance_to_dict(self)

    def to_str(self) -> str:
        """
        Convert model instance to a string.

        Returns:
            The JSON string representation of the model.

        """
        instance_dict = self.to_dict()
        return json.dumps(instance_dict)

    __str__ = to_str

    def __repr__(self) -> str:
        """Calculate the repr for the model."""
        properties = self.get_properties()
        return repr_.calculate(instance=self, properties=properties)
