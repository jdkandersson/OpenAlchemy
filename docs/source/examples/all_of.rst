allOf
=====

OpenAPI supports inheritance through the *allOf* directive.

.. seealso::

   `OpenAPI allOf documentation <https://swagger.io/docs/specification/data-models/oneof-anyof-allof-not/>`_
      OpenAPI documentation for the *allOf* directive.

   :ref:`inheritance`
      OpenAlchemy documentation for the *allOf* directive.

OpenAlchemy interprets *allOf* to mean that the schemas in the directive are to
be merged to form the final schema in place of the *allOf* directive. This
allows for re-use of general schemas for particular schemas.

Column
------

When this is done for a property of an object, a generic definition for a
property can be used as a base for properties. For example, the following
OpenAPI specification defines generic *IdBase* and *NameBase* properties
which are then used to define the *Id* and *Name* properties for the
*Employee* and *Division* schemas:

.. literalinclude:: ../../../examples/all_of/column-example-spec.yml
    :language: yaml
    :linenos:

When the specification is fed to OpenAlchemy, the *Id* and *Name* columns for
the *employee* and *division* tables are based on the *IdBase* and *NameBase*
schemas, merged with any specific directives on the respective properties of
the *Employee* and *Division* schemas. This is an implementation of the
inheritance paradigm in software engineering:

.. literalinclude:: ../../../examples/all_of/column_models.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/all_of/column_models_auto.py
    :language: python
    :linenos:

Model
-----

*allOf* also works for objects. For example, the following OpenAPI
specification defines a base schema with an *id* and *name* property. This is
then used to define the *Employee* and *Division* schemas:

.. literalinclude:: ../../../examples/all_of/model-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../examples/all_of/model_models.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/all_of/model_models_auto.py
    :language: python
    :linenos:
