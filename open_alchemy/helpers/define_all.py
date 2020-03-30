"""Define all the models with x-tablename properties."""

from .. import types
from . import schema as schema_helper


def define_all(*, model_factory: types.ModelFactory, schemas: types.Schemas) -> None:
    """
    Define all the models with x-tablename properties.

    Args:
        model_factory: Factory used to construct models.
        schemas: The schemas from which to define all.

    """
    for name, schema in schemas.items():
        if not schema_helper.constructable(schema=schema, schemas=schemas):
            continue
        model_factory(name=name)
