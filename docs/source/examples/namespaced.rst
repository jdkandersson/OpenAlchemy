Namespaced
==========

OpenAlchemy supports namespaced extension properties. The default is to prefix
extension properties with :samp:`x-`. To avoid clashes with other tools, the
:samp:`x-open-alchemy-` prefix is also supported:

.. literalinclude:: ../../../examples/namespaced/example-spec.yml
    :language: yaml
    :linenos:

The behavior of OpenAlchemy is identical.

The following example models file makes use of the OpenAPI specification to
define the SQLAlchemy models:

.. literalinclude:: ../../../examples/namespaced/models.py
    :language: python
    :linenos:

This models file instructs OpenAlchemy to construct the SQLAlchemy models
equivalent to the following traditional SQLAlchemy models.py file:

.. literalinclude:: ../../../examples/namespaced/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy also generates a fully type hinted version of the generated
SQLAlchemy models:

.. literalinclude:: ../../../examples/namespaced/models_auto.py
    :language: python
    :linenos:

.. seealso::
    :ref:`getting-started`
