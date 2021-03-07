
.. _null:

Setting the :samp:`Nullable` Property
=====================================

There are 3 methods used to determine the value of :samp:`nullable` for a
:samp:`SQLAlchemy` column. The first is the :samp:`required` property of the
schema, the second is whether the column value is generated (using, for
example, :samp:`x-autoincrement`) and the third is the :samp:`nullable`
property of an object property or the presence of :samp:`null` if :samp:`type`
is an array (consider these to be equivalent for this discussion).
:samp:`nullable` overrides :samp:`required`. If :samp:`required` would indicate
that the column is nullable but the value is generated, then it is not
nullable. The following truth table shows the logic:

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
| in list     | :samp:`X` | undefined         | False           |
+-------------+-----------+-------------------+-----------------+
| :samp:`X`   | :samp:`X` | false             | False           |
+-------------+-----------+-------------------+-----------------+
| :samp:`X`   | :samp:`X` | true              | True            |
+-------------+-----------+-------------------+-----------------+

:samp:`required` :samp:`undefined` means that the :samp:`required` property is
not defined for the schema, :samp:`not in list` means that the property is not
in the :samp:`required` list and :samp:`in list` means that the property is in
the list. :samp:`property nullable` :samp:`undefined` means that the
:samp:`nullable` property is not defined for the property, :samp:`false` and
:samp:`true` mean that :samp:`nullable` is set to :samp:`false` or
:samp:`true`, respectively. :samp:`generated` :samp:`false` means that the
column does not get automatically generated and :samp:`true` means that it
Does. Any value marked as :samp:`X` means that another value takes precedence
over the value in that case (for example, if :samp:`property nullable` is not
:samp:`undefined`, it takes precedence over both :samp:`required` and
:samp:`generated`.

.. _generated:

.. note:: To be able to include whether the column is generated in determining
    the type in the generated models file, the :samp:`x-generated` extension
    property is recorded in the schema recorded with a model.
    :samp:`x-generated` is for internal use only and should not be relied upon
    as it is subject to change.

Examples
--------

:samp:`required` :samp:`undefined`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following schema does not have the :samp:`required` property which means
that all columns have :samp:`nullable` set to :samp:`True`.

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

The following schema does not have the :samp:`required` property but the
:samp:`id` property is the primary key which is autoincremented. This means
that the :samp:`id` column is not nullable but the :samp:`name` column is
nullable.

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

:samp:`required` defined
^^^^^^^^^^^^^^^^^^^^^^^^

The following schema has the :samp:`required` property and lists the
:samp:`id` object property in the list which means that :samp:`id` has
:samp:`nullable` set to :samp:`False` and :samp:`name` has :samp:`nullable`
set to :samp:`True`.

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

:samp:`nullable` defined
^^^^^^^^^^^^^^^^^^^^^^^^

The following schema has the :samp:`nullable` property set to :samp:`false`
for one of the :samp:`id` :samp:`object` property which means that :samp:`id`
has :samp:`nullable` set to :samp:`False` and :samp:`name` has
:samp:`nullable` set to :samp:`True`.

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

:samp:`nullable` and :samp:`required` conflict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following schema has the :samp:`id` :samp:`object` property in the
:samp:`required` list but has set the :samp:`nullable` property of :samp:`id`
to :samp:`true` which means that the :samp:`id` has :samp:`nullable` set to
:samp:`True`.

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
