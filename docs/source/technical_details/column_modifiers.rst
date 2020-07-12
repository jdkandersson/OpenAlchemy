Applying Modifiers to Columns
=============================

.. _primary-key:

Primary Key
-----------

To make a column the primary key for a table, set the :samp:`x-primary-key`
property on an object property to :samp:`true`. For example:

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

To make a column auto increment, set the :samp:`x-autoincrement` property to
:samp:`true`. For example:

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
    SQLAlchemy turns :samp:`autoincrement` on by default on integer primary key
    columns. If you wish to disable autoincrement behavior, you must set
    :samp:`x-autoincrement` to :samp:`false`.

.. seealso::

    `SQLAlchemy autoincrement documentation <https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column.__init__>`_
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

To add an index to a column, set the :samp:`x-index` property on an object
property to :samp:`true`. For example:

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

This applies an index on the :samp:`name` property so that queries filtering by
name are faster.

.. _composite-index:

Composite Index
^^^^^^^^^^^^^^^

To add an index over multiple columns, set :samp:`x-composite-index` on the
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
      x-composite-index:
        - id
        - name

This defines an index over :samp:`id` and :samp:`name` to allow for faster
querying when filtering by both :samp:`id` and :samp:`name`. Use an array of
arrays to define multiple composite indexes for an object. For example:

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

This defines an index over :samp:`id` and :samp:`name` and over
:samp:`division` and :samp:`salary`. It is also possible to define a composite
index as an object which has the following properties:

* :samp:`expressions`: Defines the columns of the index.
* :samp:`name` (optional): The name of the index. Defaults to letting the database
  define the name.
* :samp:`unique` (optional): Whether to enforce a unique constraint on the
  index. Defaults to :samp:`false`.

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

To add an unique constraint to a column, set the :samp:`x-unique` property on
an object property to :samp:`true`. For example:

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

This applies a unique constraint on the :samp:`name` property which ensures
that there are no duplicate names in the database.

.. _composite-unique:

Composite Unique Constraint
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a unique constraint over multiple columns, set
:samp:`x-composite-unique` on the object. For example:

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

This applies a unique constraint over the :samp:`name` and :samp:`address`
columns to ensure an employee can be uniquely identified by their name and
place of residence. Use an array of arrays to define multiple unique
constraints for an object. For example:

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

This defines two unique constraints, one for :samp:`name` and :samp:`address`
and another for :samp:`division` and :samp:`salary`. It is also possible to
define a composite unique constraint as an object which has the following
properties:

* :samp:`columns`: Defines the columns of the unique constraint.
* :samp:`name` (optional): The name of the unique constraint. Defaults to
  letting the database define the name.

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

To add a foreign key constraint, set the :samp:`x-foreign-key` property on an
object property to the :samp:`<table name>.<column>`. For example:

.. code-block:: yaml
    :linenos:

    Division:
      type: object
      x-tablename: division
      properties:
        id:
          type: integer
        ...
    Employee:
      type: object
      x-tablename: employee
      properties:
        ...
        division_id:
          type: integer
          x-foreign-key: division.id

.. seealso::
    :ref:`relationship` shows how to define object references that result in
    relationships between tables.

.. _foreign-key-kwargs:

Foreign Key kwargs
^^^^^^^^^^^^^^^^^^

SQLAlchemy includes support for several keyword arguments for constructing
foreign keys. OpenAlchemy supports this behavior through the
:samp:`x-foreign-key-kwargs` extension property. For example, the following
foreign key constraint adds the :samp:`ondelete` keyword argument:

.. code-block:: yaml
    :linenos:

    Division:
      type: object
      x-tablename: division
      properties:
        id:
          type: integer
        ...
    Employee:
      type: object
      x-tablename: employee
      properties:
        ...
        division_id:
          type: integer
          x-foreign-key: division.id
          x-foreign-key-kwargs:
            ondelete: delete

Note that the value of :samp:`x-foreign-key-kwargs` must be an object where
keys must be a string. No further validation is done before passing the kwargs
to the SQLAlchemy foreign key constructor.

.. seealso::

    `SQLAlchemy Foreign Key kwargs <https://docs.sqlalchemy.org/en/13/core/constraints.html#sqlalchemy.schema.ForeignKey.__init__>`_
      Documentation for the keyword arguments for foreign keys in SQLAlchemy.

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

* :samp:`integer`,
* :samp:`number`,
* :samp:`string` and
* :samp:`boolean`.

Adding a default to an :samp:`object` or :samp:`array` type has no effect in
OpenAlchemy.

.. seealso::

    `SQLAlchemy "Scalar Default" <https://docs.sqlalchemy.org/en/13/core/defaults.html#scalar-defaults>`_
      Documentation for the scalar default value in SQLAlchemy.

.. _read-only:

readOnly
--------

To ensure that the value of a property is always generated server side, mark
the property as :samp:`readOnly`:

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
          readOnly: true
        name:
          type: string

The typical use case is where the :samp:`id` of an object is generated by auto
incrementing a number stored in the database. If the :samp:`id` is ever passed
to the server by a user for a table, this can cause conflict with the value
that would have been generated by the server.

OpenAlchemy uses :samp:`readOnly` to enforce that the property is not passed to
:ref:`from-dict` and :ref:`from-str`.

.. _write-only:

writeOnly
---------

To ensure that the value of a property is not returned by the server, mark the
property as :samp:`writeOnly`:

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
        passport_number:
          type: string
          writeOnly: true

The typical use case is where the value of the property only make sense to the
server or it is sensitive and should not be returned to any consumer.

OpenAlchemy skips :samp:`writeOnly` properties when converting a model instance
using :ref:`to-dict` and :ref:`to-str`.

.. _column-kwargs:

Additional kwargs
-----------------

SQLAlchemy has further keyword arguments for columns. OpenAlchemy supports
these through the :samp:`x-kwargs` extension property for a property. For
example, in the following schema, the :samp:`name` column has an additional
keyword argument :samp:`doc` added:

.. code-block:: yaml
    :linenos:

    Employee:
      type: object
      x-tablename: employee
      properties:
        ...
        name:
          type: string
          x-kwargs:
            doc: The name of the employee

Note that the following restrictions apply for :samp:`x-kwargs`:

* the value must be an object,
* the keys of the object must be strings,
* keys cannot be:

    * :samp:`nullable`,
    * :samp:`default`,
    * :samp:`primary_key`,
    * :samp:`autoincrement`,
    * :samp:`index` and
    * :samp:`unique`.

Also note that no verification, beyond the above, is done before passing the
kwargs to the SQLAlchemy column constructor.

.. seealso::

    `SQLAlchemy Column kwargs <https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column.__init__>`_
      Documentation for the keyword arguments for columns in SQLAlchemy.
