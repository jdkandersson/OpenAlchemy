Composite Unique
================

Composite unique constraints are unique constraints that span multiple columns.

.. seealso::

    :ref:`composite-unique`
      OpenAlchemy documentation for composite unique constraints.

    `SQLAlchemy Composite Unique Constraint <https://docs.sqlalchemy.org/en/13/core/constraints.html#unique-constraint>`_
      Documentation for defining composite unique constraint in SQLAlchemy.

The following example defines a composite unique constraint for the *Employee*
schema over the *address* and *division* property:

.. literalinclude:: ../../../examples/composite_unique/example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../examples/composite_unique/models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../examples/composite_unique/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/composite_unique/models_auto.py
    :language: python
    :linenos:

.. seealso::
    :ref:`getting-started`
