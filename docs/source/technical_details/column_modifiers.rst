Applying Modifiers to Columns
=============================

Primary Key
-----------

To make a column the primary key for a table, set the *x-primary-key* property
on an object property to *true*. For example:

.. code-block:: yaml

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          x-primary-key: true
        name:
          type: string

Auto Increment
--------------

To make a column auto increment, set the *x-autoincrement* property to *true*.
For example:

.. code-block:: yaml

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
    columns. You can read more here: _SQLAlchemyAutoincrement. If you wish to
    disable autoincrement behavior, you must set *x-autoincrement* to *false*.
.. _SQLAlchemyAutoincrement: https://docs.sqlalchemy.org/en/13/core/metadata.html?highlight=autoincrement#sqlalchemy.schema.Column.__init__

Index
-----

To add an index to a column, set the *x-index* property on an object property
to *true*. For example:

.. code-block:: yaml

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        name:
          type: string
          x-index: true

Unique Constraint
-----------------

To add an unique constraint to a column, set the *x-unique* property on an
object property to *true*. For example:

.. code-block:: yaml

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
        name:
          type: string
          x-unique: true

Foreign Key Constraint
----------------------

To add a foreign key constraint, set the *x-foreign-key* property on an object
property to the <table name>.<column>. For example:

.. code-block:: yaml

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
