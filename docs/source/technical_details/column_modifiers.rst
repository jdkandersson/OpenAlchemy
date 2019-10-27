Applying Modifiers to Columns
=============================

.. _primary-key:

Primary Key
-----------

To make a column the primary key for a table, set the *x-primary-key* property
on an object property to *true*. For example:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          x-primary-key: true
        name:
          type: string

.. _autoincrement:

Auto Increment
--------------

To make a column auto increment, set the *x-autoincrement* property to *true*.
For example:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          x-primary-key: true
          x-autoincrement: true
        name:
          type: string

.. note::
    SQLAlchemy turns *autoincrement* on by default on integer primary key
    columns. If you wish to
    disable autoincrement behavior, you must set *x-autoincrement* to *false*.

.. seealso::

   `SQLAlchemy autoincrement documentation <https://docs.sqlalchemy.org/en/13/core/metadata.html?highlight=autoincrement#sqlalchemy.schema.Column.__init__>`_
      Documentation for SQLAlchemy autoincrement.

.. _index:

Index
-----

To add an index to a column, set the *x-index* property on an object property
to *true*. For example:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        name:
          type: string
          x-index: true

.. _unique:

Unique Constraint
-----------------

To add an unique constraint to a column, set the *x-unique* property on an
object property to *true*. For example:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        name:
          type: string
          x-unique: true

.. _foreign-key:

Foreign Key Constraint
----------------------

To add a foreign key constraint, set the *x-foreign-key* property on an object
property to the <table name>.<column>. For example:

.. code-block:: yaml
   :linenos:

   Division:
      type: object
      x-tablename: division
      properties:
        id:
          type: integer
        name:
          type: string
          x-unique: true
   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        name:
          type: string
        division_id:
          type: integer
          x-foreign-key: division.id

.. seealso::
    :ref:`relationship` shows how to define object references that result in
    relationships between tables.
