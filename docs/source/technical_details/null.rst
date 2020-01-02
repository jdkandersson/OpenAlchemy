.. contents::

.. _null:

Setting the *Nullable* Property
===============================

There are 3 methods used to determine the value of *nullable* for a
*SQLAlchemy* column. The first is the *required* property of the schema, the
second is whether the column value is generated (using, for example,
*x-autoincrement*) and the third is the *nullable* property of an object
property. *nullable* overrides *required*. If *required* would indicate that
the column is nullable but the value is generated, then it is not nullable. The
following truth table shows the logic:

+-------------+-----------+-------------------+-----------------+
| required    | generated | property nullable | column nullable |
+=============+===========+===================+=================+
| undefined   | false     | undefined         | True            |
+-------------+-----------+-------------------+-----------------+
| undefined   | true      | undefined         | False           |
+-------------+-----------+-------------------+-----------------+
| not in list | false     | undefined         | True            |
+-------------+-----------+-------------------+-----------------+
| not in list | true      | undefined         | False           |
+-------------+-----------+-------------------+-----------------+
| in list     | *X*       | undefined         | False           |
+-------------+-----------+-------------------+-----------------+
| *X*         | *X*       | false             | False           |
+-------------+-----------+-------------------+-----------------+
| *X*         | *X*       | true              | True            |
+-------------+-----------+-------------------+-----------------+

*required* *undefined* means that the *required* property is not defined for
the schema, *not in list* means that the property is not in the *required*
list and *in list* means that the property is in the list.
*property nullable* *undefined* means that the *nullable* property is not
defined for the property, *false* and *true* mean that *nullable* is set to
*false* or *true*, respectively. *generated* *false* means that the column
does not get automatically generated and *true* means that it does. Any value
marked as *X* means that another value takes precedence over the value in
that case (for example, if *property nullable* is not *undefined*, it takes
precedence over both *required* and *generated*.

.. _generated:

.. note:: To be able to include whether the column is generated in determining
    the type in the generated models file, the *x-generated* extension property
    is recorded in the schema recorded with a model. *x-generated* is for
    internal use only and should not be relied upon as it is subject to change.

Examples
--------

*required* *undefined*
^^^^^^^^^^^^^^^^^^^^^^

The following schema does not have the *required* property which means that all
columns have *nullable* set to *True*.

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

generated
^^^^^^^^^

The following schema does not have the *required* property but the *id*
property is the primary key which is autoincremented. This means that the *id*
column is not nullable but the *name* column is nullable.

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

*required* defined
^^^^^^^^^^^^^^^^^^

The following schema has the *required* property and lists the *id* object
property in the list which means that *id* has *nullable* set to *False* and
*name* has *nullable* set to *True*.

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
      required:
        - id

*nullable* defined
^^^^^^^^^^^^^^^^^^

The following schema has the *nullable* property set to *false* for one of the
*id* *object* property which means that *id* has *nullable* set to *False* and
*name* has *nullable* set to *True*.

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          nullable: false
        name:
          type: string

*nullable* and *required* conflict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following schema has the *id* *object* property in the *required* list but
has set the *nullable* property of *id* to *true* which means that the *id* has
*nullable* set to *True*.

.. code-block:: yaml
   :linenos:

   Employee:
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          nullable: true
        name:
          type: string
      required:
        - id
