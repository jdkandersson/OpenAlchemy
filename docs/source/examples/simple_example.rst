Simple
======

To illustrate the purpose of the OpenAlchemy package, the following example
OpenAPI specification defines an endpoint to retrieve the employees of a
company:

.. literalinclude:: ../../../examples/simple/example-spec.yml
    :language: yaml
    :linenos:


It is common to store data to fulfill such an endpoint in a database, for which
OpenAlchemy can be used to re-use the schemas from the OpenAPI specification
to define the database schemas with the help of certain extension properties.

.. seealso::
    :ref:`how-does-it-work`

The following example models file makes use of the OpenAPI specification to
define the SQLAlchemy models:

.. literalinclude:: ../../../examples/simple/models.py
    :language: python
    :linenos:

This models file instructs OpenAlchemy to construct the SQLAlchemy models
equivalent to the following traditional SQLAlchemy models.py file:

.. literalinclude:: ../../../examples/simple/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy also generates a fully type hinted version of the generated
SQLAlchemy models:

.. literalinclude:: ../../../examples/simple/models_auto.py
    :language: python
    :linenos:

This allows for autocomplete on the model initialization:

.. image:: ../../../examples/simple/models_autocomplete_init.png

and it also enables autocomplete on instance variables:

.. image:: ../../../examples/simple/models_autocomplete_instance.png
