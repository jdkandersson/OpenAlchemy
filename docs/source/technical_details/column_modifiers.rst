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

Indexes can be added at the column level and at the object level. At the column
level, the index is applied on a single column. At the object level, an index
can be defined over multiple columns.

.. _column-index:

Column Index
^^^^^^^^^^^^

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

This applies an index on the *name* property so that queries filtering by name
are faster.

.. _composite-index:

Composite Index
^^^^^^^^^^^^^^^

To add an index over multiple columns, set *x-composite-index* on the object.
For example:

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
      x-composite-index:
        - id
        - name

This defines an index over *id* and *name* to allow for faster querying when
filtering by both *id* and *name*. Use an array of arrays to define multiple
composite indexes for an object. For example:

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
        division:
          type: string
        salary:
          type: number
      x-composite-index:
        - - id
          - name
        - - division
          - salary

This defines an index over *id* and *name* and over *division* and *salary*. It
is also possible to define a composite index as an object which has the
following properties:

* *expressions*: Defines the columns of the index.
* *name* (optional): The name of the index. Defaults to letting the database
  define the name.
* *unique* (optional): Whether to enforce a unique constraint on the index.
  Defaults to *false*.

For example:

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
      x-composite-index:
        name: ix_employee_id_name
        expressions:
          - id
          - name
        unique: true

It is also possible to define multiple composite indexes as an array of
objects. For example:

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
        division:
          type: string
        salary:
          type: number
      x-composite-index:
        - name: ix_employee_id_name
          expressions:
            - id
            - name
        - name: ix_employee_division_salary
          expressions:
            - division
            - salary

.. seealso::

   `SQLAlchemy Composite Index <https://docs.sqlalchemy.org/en/13/core/constraints.html#index-api>`_
      Documentation for defining composite indexes in SQLAlchemy.

.. _unique:

Unique Constraint
-----------------

Unique constraints can be added at the column level and at the object level. At
the column level, the constraint is applied on a single column. At the object
level, a constraint can be defined over multiple columns.

.. _column-unique:

Column Unique Constraint
^^^^^^^^^^^^^^^^^^^^^^^^

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

This applies a unique constraint on the *name* property which ensures that
there are no duplicate names in the database.

.. _composite-unique:

Composite Unique Constraint
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a unique constraint over multiple columns, set *x-composite-unique* on
the object. For example:

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
        address:
          type: string
      x-composite-unique:
        - name
        - address

This applies a unique constraint over the *name* and *address* columns to
ensure an employee can be uniquely identified by their name and place of
residence. Use an array of arrays to define multiple unique constraints for an
object. For example:

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
        address:
          type: string
        division:
          type: string
        salary:
          type: number
      x-composite-unique:
        - - name
          - address
        - - division
          - salary

This defines two unique constraints, one for *name* and *address* and another
for *division* and *salary*. It is also possible to define a composite unique
constraint as an object which has the following properties:

* *columns*: Defines the columns of the unique constraint.
* *name* (optional): The name of the unique constraint. Defaults to letting the
  database define the name.

For example:

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
        address:
          type: string
      x-composite-unique:
        name: uq_employee_name_address
        columns:
          - name
          - address

It is also possible to define multiple unique constraints as an array of
objects. For example:

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
        address:
          type: string
        division:
          type: string
        salary:
          type: number
      x-composite-unique:
        - name: uq_employee_name_address
          columns:
            - name
            - address
        - name: uq_employee_division_salary
          columns:
            - division
            - salary

.. seealso::

   `SQLAlchemy Composite Unique Constraint <https://docs.sqlalchemy.org/en/13/core/constraints.html#unique-constraint>`_
      Documentation for defining composite unique constraint in SQLAlchemy.

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

.. _default:

Default
-------

To add a default value for a column use the OpenAPI default property:

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
          default: Unknown

The default value is added to the column constructor as the default value as a
"Scalar Default" in SQLAlchemy. The following property types support a default
value (including all their formats supported by OpenAlchemy):

* *integer*,
* *number*,
* *string* and
* *boolean*.

Adding a default to an *object* or *array* type has no effect in OpenAlchemy.

.. seealso::

   `SQLAlchemy "Scalar Default" <https://docs.sqlalchemy.org/en/13/core/defaults.html#scalar-defaults>`_
      Documentation for the scalar default value in SQLAlchemy.
