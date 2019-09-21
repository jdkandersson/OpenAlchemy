.. _inheritance:

Inheritance
===========

By default, re-using SQLAlchemy models through inheritance is not simple as
SQLAlchemy uses inheritance for other purposes. openapi-SQLAlchemy supports
model inheritance using the *allOf* statement from openapi. Currently column
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

.. literalinclude:: ../../../examples/all-of-example-spec.yml

The SQLAlchemy models might then look like:

.. literalinclude:: ../../../examples/all_of_models.py

.. seealso::
    :ref:`references` shows how to reference to other schemas.
