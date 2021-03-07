Nullable
========

A property can be set to be nullable using the :samp:`nullable` property for
OpenAPI 3.0:

.. literalinclude:: ../../../examples/nullable/openapi-3-0/example-spec.yml
    :language: yaml
    :linenos:

Or by including :samp:`null` in the :samp:`type` array for OpenAPI 3.1:

.. literalinclude:: ../../../examples/nullable/openapi-3-1/example-spec.yml
    :language: yaml
    :linenos:

The following example models file makes use of the OpenAPI specification to
define the SQLAlchemy models:

.. literalinclude:: ../../../examples/nullable/openapi-3-1/models.py
    :language: python
    :linenos:

This models file instructs OpenAlchemy to construct the SQLAlchemy models
equivalent to the following traditional SQLAlchemy models.py file:

.. literalinclude:: ../../../examples/nullable/openapi-3-1/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy also generates a fully type hinted version of the generated
SQLAlchemy models:

.. literalinclude:: ../../../examples/nullable/openapi-3-1/models_auto.py
    :language: python
    :linenos:

.. seealso::
    :ref:`getting-started`
