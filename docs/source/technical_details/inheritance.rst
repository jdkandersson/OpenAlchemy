.. _inheritance:

Inheritance
===========

By default, re-using SQLAlchemy models through inheritance is not simple as
SQLAlchemy uses inheritance for other purposes. OpenAlchemy supports
model inheritance using the :samp:`allOf` statement from OpenAPI. Currently
column and model inheritance is supported.

.. seealso::

    `SQLAlchemy inheritance documentation <https://docs.sqlalchemy.org/en/13/orm/inheritance.html>`_
      Documentation for SQLAlchemy inheritance.

Column Inheritance
------------------

For columns, the main purpose of using inheritance through :samp:`allOf` is to
re-use elements of a base column definition but customize certain properties.
For example, you might have an integer :samp:`id` column for many models that
is quite similar except for the description. Or you might have a string
:samp:`name` column on many models but where the description and example might
differ. For example, the following specification defines a base schema for the
:samp:`id` and :samp:`name` columns and re-uses them for the :samp:`Employee`
and :samp:`Division` models with some changes to the description, example or
both.

.. literalinclude:: ../../../examples/all_of/column-example-spec.yml
    :language: yaml
    :linenos:

The SQLAlchemy models might then look like:

.. literalinclude:: ../../../examples/all_of/column_models.py
    :language: python
    :linenos:

Any duplicate properties are overridden by subsequent entries in :samp:`allOf`.
For example, if all entries have the :samp:`description` property, the
:samp:`description` from the last entry is actually used.

Model Inheritance
-----------------

A similar feature is also supported for models. This allows, for example, to
define a base model that has an :samp:`id` and :samp:`name`. Then other models
with :samp:`id` and :samp:`name` columns can use the :samp:`allOf` feature to
copy those columns and add any model specific columns. This reduces duplication
in specifications. For example, the following specification defines an
:samp:`IdNameBase` model with :samp:`id` and :samp:`name` columns.
:samp:`Employee` and :samp:`Division` also required the columns but the
:samp:`description` and *x-tablename* needs to be different. By using
:samp:`allOf` they can copy the :samp:`id` and :samp:`name` columns from
:samp:`IdNameBase` and define their own :samp:`description` and
:samp:`tablename`.

.. literalinclude:: ../../../examples/all_of/model-example-spec.yml
    :language: yaml
    :linenos:

The SQLAlchemy models might then look like:

.. literalinclude:: ../../../examples/all_of/model_models.py
    :language: python
    :linenos:

Similar rules as for columns apply for duplicate properties in :samp:`allOf`
entries with one difference. The :samp:`required` property is treated as an
aggregate of all entries. For example, if the first entry has :samp:`id` and
the second entry has :samp:`name` in the required list, the final specification
has both :samp:`id` and :samp:`name` in the required list.

.. seealso::
    :ref:`references` shows how to reference to other schemas.

.. _joined-table-inheritance:

Joined Table Inheritance
------------------------

SQLAlchemy includes a feature where a model class hierarchy is implemented by
giving each class it's own table. For example, an :samp:`Employee` might have
an :samp:`id`, :samp:`name` and :samp:`type`. Then a :samp:`Manager` model
might be defined that derives from :samp:`Employee` and adds the
:samp:`manager_data` column. This is also supported by OpenAlchemy through a
combination of the :samp:`x-inherits` and :samp:`x-kwargs` extension
properties. The :samp:`x-kwargs` has already been discussed here:
:ref:`model-kwargs` and will be used to define some special model parameters to
instruct SQLAlchemy how to map :samp:`Manager` to :samp:`Employee`.

.. _x-inherits:

:samp:`x-inherits`
^^^^^^^^^^^^^^^^^^

The :samp:`x-inherits` extension property is used to indicate to OpenAlchemy
that a schema inherits from another schema. The following values are supported:

* :samp:`boolean`:
    * :samp:`true`: Indicates that the schema inherits from the closest schema
      that it has a :samp:`$ref` to that can be constructed. Object schemas
      with the :samp:`x-tablename` or :samp:`x-inherits` are those that
      generally can be constructed.
    * :samp:`false`: Indicates that the schema does not inherit.
* :samp:`string`: The name of the parent schema. The schema must have a
  :samp:`$ref` that links it to the schema with the name of :samp:`x-inherits`.

In any case, if a schema inherits from another schema, there must be a
:samp:`$ref` linking the two schemas. That can be contained in :samp:`allOf`
and could be behind any number of nested :samp:`$ref`.

.. seealso::
    :ref:`references` shows how to reference to other schemas.

:samp:`x-kwargs`
^^^^^^^^^^^^^^^^

The required :samp:`__mapper_args__` must be added using :samp:`x-kwargs`. For
example, for :samp:`Employee`:

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      ...
      x-kwargs:
        __mapper_args__:
          polymorphic_on: type
          polymorphic_identity: employee

And for :samp:`Manager`:

.. code-block:: yaml
   :linenos:

    Manager:
      type: object
      ...
      x-kwargs:
        __mapper_args__:
          polymorphic_identity: manager

Example
^^^^^^^

The following shows the :samp:`Employee` and :samp:`Manager` schemas required
to define joined table inheritance in OpenAlchemy:

.. code-block:: yaml
   :linenos:

    Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          x-primary-key: true
        ...
        type:
          type: string
          description: The type of the employee.
          example: employee
      x-kwargs:
        __mapper_args__:
          polymorphic_on: type
          polymorphic_identity: employee
    Manager:
      allOf:
        - $ref: "#/components/schemas/Employee"
        - x-inherits: true
          x-tablename: manager
          type: object
          properties:
            id:
              type: integer
              x-primary-key: true
              x-foreign-key: employee.id
            manager_data:
              type: string
          x-kwargs:
            __mapper_args__:
              polymorphic_identity: manager

.. _single-table-inheritance:

Single Table Inheritance
------------------------

Single table inheritance is very similar to :ref:`joined-table-inheritance`
with the difference that all classes are linked to the same table and there is
no foreign key relationship between the models. The following shows the
:samp:`Employee` and :samp:`Manager` schemas required to define single table
inheritance in OpenAlchemy:

.. code-block:: yaml
   :linenos:

    Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          x-primary-key: true
        ...
        type:
          type: string
          description: The type of the employee.
          example: employee
      x-kwargs:
        __mapper_args__:
          polymorphic_on: type
          polymorphic_identity: employee
    Manager:
      allOf:
        - $ref: "#/components/schemas/Employee"
        - x-inherits: true
          type: object
          properties:
            manager_data:
              type: string
          x-kwargs:
            __mapper_args__:
              polymorphic_identity: manager

.. seealso::

    `SQLAlchemy single table inheritance documentation <https://docs.sqlalchemy.org/en/13/orm/inheritance.html?highlight=single%20table#single-table-inheritance>`_
      Documentation for SQLAlchemy single table inheritance.
