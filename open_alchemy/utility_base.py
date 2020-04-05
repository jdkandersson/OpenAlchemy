"""Base class providing utilities for SQLAlchemy models."""

import functools
import json
import typing

from . import exceptions
from . import facades
from . import helpers
from . import types

TUtilityBase = typing.TypeVar("TUtilityBase", bound="UtilityBase")
TOptUtilityBase = typing.Optional[TUtilityBase]


class UtilityBase:
    """Base class providing utilities for SQLAlchemy models."""

    # Record of the schema used to construct the model. Myst be an object type. For all
    # columns any $ref must be resolved an allOf must be merged for all. Objects must
    # be recorded as a free-form object and have a x-de-$ref extension property with
    # the de-referenced name of the schema.
    _schema: typing.ClassVar[types.Schema]

    def __init__(self, **kwargs: typing.Any) -> None:
        """Construct."""
        raise NotImplementedError

    @classmethod
    def _get_schema(cls) -> types.Schema:
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
    def get_properties(cls) -> types.Schema:
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

    @staticmethod
    def _get_model(
        *, spec: types.Schema, name: str, schema: types.Schema
    ) -> typing.Type[TUtilityBase]:
        """Get the model based on the schema."""
        ref_model_name = helpers.ext_prop.get(source=spec, name="x-de-$ref")
        if ref_model_name is None:
            raise exceptions.MalformedSchemaError(
                "To construct object parameters the schema for the property must "
                "include the x-de-$ref extension property with the name of the "
                "model to construct for the property. "
                f"The property is {name}. "
                f"The model schema is {json.dumps(schema)}."
            )
        # Try to get model
        ref_model: TOptUtilityBase = facades.models.get_model(name=ref_model_name)
        if ref_model is None:
            raise exceptions.SchemaNotFoundError(
                f"The {ref_model_name} model was not found on open_alchemy.models."
            )
        return ref_model

    @staticmethod
    def _get_parent(*, schema: types.Schema) -> typing.Type[TUtilityBase]:
        """Get the parent model of a model."""
        parent_name = helpers.ext_prop.get(source=schema, name="x-inherits")
        if parent_name is None or not isinstance(parent_name, str):
            raise exceptions.MalformedSchemaError(
                "To construct a model that inherits x-inherits must be present and a "
                "string. "
                f"The model schema is {json.dumps(schema)}."
            )
        # Try to get model
        parent: TOptUtilityBase = facades.models.get_model(name=parent_name)
        if parent is None:
            raise exceptions.SchemaNotFoundError(
                f"The {parent_name} model was not found on open_alchemy.models."
            )
        return parent

    @staticmethod
    def _model_from_dict(
        kwargs: typing.Dict[str, typing.Any], *, model: typing.Type[TUtilityBase]
    ) -> TUtilityBase:
        """Construct model from dictionary."""
        return model.from_dict(**kwargs)

    @classmethod
    def construct_from_dict_init(
        cls: typing.Type[TUtilityBase], **kwargs: typing.Any
    ) -> typing.Dict[str, typing.Any]:
        """Construct the dictionary passed to model construction."""
        # Check dictionary
        schema = cls._get_schema()
        try:
            facades.jsonschema.validate(instance=kwargs, schema=schema)
        except facades.jsonschema.ValidationError:
            raise exceptions.MalformedModelDictionaryError(
                "The dictionary passed to from_dict is not a valid instance of the "
                "model schema. "
                f"The expected schema is {json.dumps(schema)}. "
                f"The given value is {json.dumps(kwargs)}."
            )

        # Assemble dictionary for construction
        properties = cls.get_properties()
        model_dict: typing.Dict[str, typing.Any] = {}
        for name, value in kwargs.items():
            # Get the specification and type of the property
            spec = properties.get(name)
            if spec is None:
                raise exceptions.MalformedModelDictionaryError(
                    "A parameter was passed in that is not a property in the model "
                    "schema. "
                    f"The parameter is {name}. "
                    f"The model schema is {json.dumps(schema)}."
                )

            # Check readOnly
            read_only = spec.get("readOnly")
            if read_only is True:
                raise exceptions.MalformedModelDictionaryError(
                    "A parameter was passed in that is marked as readOnly in the "
                    "schema. "
                    f"The parameter is {name}. "
                    f"The model schema is {json.dumps(schema)}."
                )

            # Check type
            type_ = spec.get("type")
            format_ = spec.get("format")
            if type_ is None:
                raise exceptions.TypeMissingError(
                    f"The schema for the {name} property does not have a type."
                )

            # Handle object
            ref_model: typing.Type[UtilityBase]
            if type_ == "object":
                ref_model = cls._get_model(spec=spec, name=name, schema=schema)
                ref_model_instance = cls._model_from_dict(value, model=ref_model)
                model_dict[name] = ref_model_instance
                continue

            if type_ == "array":
                item_spec = spec.get("items")
                if item_spec is None:
                    raise exceptions.MalformedSchemaError(
                        "To construct array parameters the schema for the property "
                        "must include the items property with the information about "
                        "the array items. "
                        f"The property is {name}. "
                        f"The model schema is {json.dumps(schema)}."
                    )
                ref_model = cls._get_model(spec=item_spec, name=name, schema=schema)
                model_from_dict = functools.partial(
                    cls._model_from_dict, model=ref_model
                )
                ref_model_instances = map(model_from_dict, value)
                model_dict[name] = list(ref_model_instances)
                continue

            # Handle other types
            model_dict[name] = helpers.oa_to_py_type.convert(
                value=value, type_=type_, format_=format_
            )

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
                f"The value is not of type string. The value is {value}."
            )
        try:
            dict_value = json.loads(value)
        except json.JSONDecodeError:
            raise exceptions.MalformedModelDictionaryError(
                f"The string value is not valid JSON. The value is {value}."
            )
        if not isinstance(dict_value, dict):
            raise exceptions.MalformedModelDictionaryError(
                f"The string value is not a Python dictionary. The value is {value}."
            )
        return cls.from_dict(**dict_value)

    @staticmethod
    def _object_to_dict_relationship(
        *, value: typing.Any, name: str
    ) -> typing.Dict[str, typing.Any]:
        """Call to_dict on relationshup object."""
        try:
            return value.to_dict()
        except AttributeError:
            raise exceptions.InvalidModelInstanceError(
                f"The {name} object property instance does not have a to_dict "
                "implementation."
            )
        except TypeError:
            raise exceptions.InvalidModelInstanceError(
                f"The {name} object property instance to_dict implementation is "
                "expecting arguments."
            )

    @staticmethod
    def _object_to_dict_read_only(
        *, value: typing.Any, spec: types.Schema, name: str
    ) -> typing.Dict[str, typing.Any]:
        """Convert relationship to dictionary based on spec."""
        properties = spec.get("properties")
        if properties is None:
            raise exceptions.MalformedSchemaError(
                f"readOnly object definition {name} must have properties."
            )
        if not properties:
            raise exceptions.MalformedSchemaError(
                f"readOnly object definitions {name} must have at least 1 property."
            )
        return_dict = {}
        for key in properties.keys():
            return_dict[key] = getattr(value, key, None)
        return return_dict

    @classmethod
    def _object_to_dict(
        cls, value, name: str, spec: types.Schema, read_only: bool
    ) -> typing.Dict[str, typing.Any]:
        """Call to_dict on object."""
        if not read_only:
            return cls._object_to_dict_relationship(value=value, name=name)
        return cls._object_to_dict_read_only(value=value, name=name, spec=spec)

    @staticmethod
    def _simple_type_to_dict(
        *, format_: typing.Optional[str], value: typing.Any
    ) -> typing.Any:
        """
        Convert values with basic types to dictionary keys.

        Args:
            format_: The format of the value.
            value: The value to convert.

        Returns:
            The value converted to the expected dictionary key.

        """
        # Handle other types
        if format_ == "date":
            return value.isoformat()
        if format_ == "date-time":
            return value.isoformat()
        if format_ == "binary":
            return value.decode()
        return value

    @classmethod
    def to_dict_property(
        cls,
        value: typing.Any,
        *,
        spec: types.Schema,
        name: str,
        array_context: bool = False,
        read_only: bool = False,
    ) -> typing.Any:
        """
        Perform property level to dict operation.

        Args:
            value: The value of the property.
            spec: The specification for the property.
            name: The name of the property.
            array_context: Whether array items are being worked on.
            read_only: Whether a readOnly property is being worked on.

        Returns:
            property value.

        """
        if not read_only:
            read_only = spec.get("readOnly", read_only)
        try:
            type_ = helpers.peek.type_(schema=spec, schemas={})
        except exceptions.TypeMissingError:
            schema_descriptor = "array item" if array_context else "property"
            raise exceptions.TypeMissingError(
                f"The {schema_descriptor} schema for the {name} property does not have "
                f"a type. The {schema_descriptor} schema is {json.dumps(spec)}."
            )
        format_ = helpers.peek.format_(schema=spec, schemas={})

        # Handle array
        if type_ == "array":
            if array_context:
                raise exceptions.MalformedSchemaError(
                    "The array item schema cannot have the array type."
                )
            if value is None:
                return []
            item_spec = spec.get("items")
            if item_spec is None:
                raise exceptions.MalformedSchemaError(
                    "The array item schema must have an items property."
                )
            to_dict_property = functools.partial(
                cls.to_dict_property,
                spec=item_spec,
                name=name,
                array_context=True,
                read_only=read_only,
            )
            array_dict_values = map(to_dict_property, value)
            return list(array_dict_values)

        if value is None:
            return None

        # Handle object
        if type_ == "object":
            return cls._object_to_dict(
                value=value, name=name, spec=spec, read_only=read_only
            )

        # Handle other types
        return cls._simple_type_to_dict(format_=format_, value=value)

    @classmethod
    def instance_to_dict(cls, instance: TUtilityBase) -> typing.Dict[str, typing.Any]:
        """Convert instance of the model to a dictionary."""
        properties = cls.get_properties()

        # Collecting the values of the properties
        return_dict: typing.Dict[str, typing.Any] = {}
        for name, spec in properties.items():
            value = getattr(instance, name, None)
            return_dict[name] = instance.to_dict_property(
                spec=spec, name=name, value=value
            )

        return return_dict

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Convert model instance to dictionary.

        Raise TypeMissingError if a property does not have a type.
        Raise InvalidModelInstanceError is an object to_dict call failed.

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
