References
==========

OpenAPI supports referencing other sections of the schema using *$ref*.
OpenAlchemy interprets this by substituting the reference with the referenced
schema before constructing.

.. seealso::

    `OpenAPI $ref Documentation <https://swagger.io/docs/specification/using-ref/>`_
      Documentation for the OpenAPI *$ref* directive.

    :ref:`references`
      OpenAlchemy documentation for references.

Column
------

The following example defines *Id*, *Name* and *Division* schemas which are
used for the respective properties of the *Employee* schema:

.. literalinclude:: ../../../examples/ref/column-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../examples/ref/column_models.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/ref/column_models_auto.py
    :language: python
    :linenos:

Model
------

The following example defines the schema of an employee in *RefEmployee* and
then defines the schema of *Employee* to be the same as *RefEmployee*:

.. literalinclude:: ../../../examples/ref/model-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../examples/ref/model_models.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/ref/model_models_auto.py
    :language: python
    :linenos:
