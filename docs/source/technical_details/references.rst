.. _references:

References
==========

Using *$ref* statements, *OpenAPI* allows you to reference other parts of the
schemas section. This means that a single definition for a *property* of an
*object* can be used for multiple *objects*. This pattern is supported by
*OpenAPI-SQLAlchemy*. For example, the following *OpenAPI* specification makes
use of references:

.. literalinclude:: ../../../examples/ref-column-example-spec.yml

Which leads to the following *models.py* file:

.. literalinclude:: ../../../examples/ref_column_models.py

The same is also possible for whole models which allows for aliases for models:

.. literalinclude:: ../../../examples/ref-model-example-spec.yml

Which leads to the following *models.py* file:

.. literalinclude:: ../../../examples/ref_model_models.py

.. seealso::
    :ref:`relationship` shows how to define object references that result in
    relationships between tables.

    :ref:`inheritance` shows how to use inheritance for schemas.
