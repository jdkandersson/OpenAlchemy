"""Define all the models with x-tablename properties."""

from .. import types
from . import inheritance as inheritance_helper
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
        if schema_helper.inherits(schema=schema, schemas=schemas):
            parents = inheritance_helper.get_parents(schema=schema, schemas=schemas)
            for parent in parents:
                model_factory(name=parent)
        model_factory(name=name)
