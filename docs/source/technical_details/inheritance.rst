.. _inheritance:

Inheritance
===========

By default, re-using SQLAlchemy models through inheritance is not simple as
SQLAlchemy uses inheritance for other purposes. OpenAlchemy supports
model inheritance using the *allOf* statement from OpenAPI. Currently column
inheritance is supported, model inheritance is planned for the future.

.. seealso::

   `SQLAlchemy inheritance documentation <https://docs.sqlalchemy.org/en/13/orm/inheritance.html>`_
      Documentation for SQLAlchemy inheritance.

Column Inheritance
------------------

For columns, the main purpose of using inheritance through *allOf* is to
re-use elements of a base column definition but customize certain properties.
For example, you might have an integer *id* column for many models that is
quite similar except for the description. Or you might have a string *name*
column on many models but where the description and example might differ. For
example, the following specification defines a base schema for the *id* and
*name* columns and re-uses them for the *Employee* and *Division* models with
some changes to the description, example or both.

.. literalinclude:: ../../../examples/all-of-column-example-spec.yml

The SQLAlchemy models might then look like:

.. literalinclude:: ../../../examples/all_of_column_models.py

Any duplicate properties are overridden by subsequent entries in *allOf*. For
example, if all entries have the *description* property, the *description* from
the last entry is actually used.

Model Inheritance
-----------------

A similar feature is also supported for models. This allows, for example, to
define a base model that has an *id* and *name*. Then other models with *id*
and *name* columns can use the *allOf* feature to copy those columns and add
any model specific columns. This reduces duplication in specifications. For
example, the following specification defines an *IdNameBase* model with *id*
and *name* columns. *Employee* and *Division* also required the columns but
the *description* and *x-tablename* needs to be different. By using *allOf*
they can copy the *id* and *name* columns from *IdNameBase* and define their
own *description* and *tablename*.

.. literalinclude:: ../../../examples/all-of-model-example-spec.yml

The SQLAlchemy models might then look like:

.. literalinclude:: ../../../examples/all_of_model_models.py

Similar rules as for columns apply for duplicate properties in *allOf* entries
with one difference. The *required* property is treated as an aggregate of all
entries. For example, if the first entry has *id* and the second entry has
*name* in the required list, the final specification has both *id* and *name*
in the required list.

.. seealso::
    :ref:`references` shows how to reference to other schemas.
