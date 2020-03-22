.. _references:

References
==========

Using *$ref* statements, *OpenAPI* allows you to reference other parts of the
schemas section. This means that a single definition for a *property* of an
*object* can be used for multiple *objects*. This pattern is supported by
*OpenAlchemy*. For example, the following *OpenAPI* specification makes
use of references:

.. literalinclude:: ../../../examples/ref/column-example-spec.yml
    :language: yaml
    :linenos:

Which leads to the following *models.py* file:

.. literalinclude:: ../../../examples/ref/column_models.py
    :language: python
    :linenos:

The same is also possible for whole models which allows for aliases for models:

.. literalinclude:: ../../../examples/ref/model-example-spec.yml
    :language: yaml
    :linenos:

Which leads to the following *models.py* file:

.. literalinclude:: ../../../examples/ref/model_models.py
    :language: python
    :linenos:

.. seealso::
    :ref:`relationship` shows how to define object references that result in
    relationships between tables.

    :ref:`inheritance` shows how to use inheritance for schemas.

Remote References
-----------------

The OpenAPI specification supports remote references in

1. another file within the file system and
2. a file available at a URL.

For (1), the following example shows how to reference a schema in another file:

.. literalinclude:: ../../../examples/remote/example-spec.yml
    :language: yaml
    :linenos:

The schema in the remote file is unchanged:

.. literalinclude:: ../../../examples/remote/remote-example-spec.yml
    :language: yaml
    :linenos:

For (2), the following example shows how to reference a schema at a URL:

.. literalinclude:: ../../../examples/remote/url-example-spec.yml
    :language: yaml
    :linenos:

For a schema to be picked up by *OpenAlchemy*, it must have an entry in the
*#/components/schemas/...* object. Remote references from within a schema are
also supported.
