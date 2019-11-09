"""Types shared across modules."""

import typing

import typing_extensions

Schema = typing.Dict[str, typing.Any]
Schemas = typing.Dict[str, Schema]
AllOfSpec = typing.List[Schema]


class ModelFactory(typing_extensions.Protocol):
    """Defines interface for model factory."""

    def __call__(self, *, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


class ModelClass(typing_extensions.Protocol):
    """Defines interface for model factory."""

    _schema: Schema

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

    def to_dict(self) -> typing.Dict:
        """Convert model instance to dictionary."""
        ...


# Unique consraint types
ColumnList = typing.List[str]
ColumnListList = typing.List[ColumnList]
Unique = typing.Dict[str, typing.Any]
UniqueList = typing.List[Unique]
AnyUnique = typing.Union[ColumnList, ColumnListList, Unique, UniqueList]
# Index types
Index = typing.Dict[str, typing.Any]
IndexList = typing.List[Index]
AnyIndex = typing.Union[ColumnList, ColumnListList, Index, IndexList]
