.. _relationship:

Defining Relationships
======================

Defining relationships between tables is done by using *$ref* to reference
other objects from an object property.

.. seealso::

   `SQLAlchemy relationship documentation <https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html>`_
      Documentation for SQLAlchemy relationships.

Many to One
-----------

The following *OpenAPI* specification defines a many to one relationship:

.. literalinclude:: ../../../examples/relationship-many-to-one-example-spec.yml
    :language: yaml
    :linenos:

By adding a *$ref* to an object property that points at another object, a
relationship with the logical name will be formed. For example, if the *$ref*
points to the *Division* object, *sqlalchemy.orm.relationship* with
*"Division"* will be called. Note that you must add both objects to the
*models.py* file. For example:

.. literalinclude:: ../../../examples/relationship_many_to_one_models.py
    :language: python
    :linenos:

Alongside the *relationship*, a foreign key will also be added to the table
with the *$ref* property under the name of the property suffixed with *_id*.
Note that, the object being referenced must have the *id* property.

The only way to make the foreign key column not nullable is to add the
property with the reference to the *required* list.

Without OpenLAlchemy, the following is the equivalent *models.py* file:

.. literalinclude:: ../../../examples/relationship_many_to_one_models_traditional.py
    :language: python
    :linenos:


.. _backref:

Backref
^^^^^^^

One of the features of *SQLAlchemy* is that a relationship can be back
populated to the referred table. This is supported using the *x-backref*
key. There are 2 places where the *x-backref* key can be defined. The
recommended implementation adds it using *allOf*:

.. literalinclude:: ./relationships/many_to_one/backref_recommended.yaml
    :language: yaml
    :linenos:

Note that, when *allOf* is used, there must be exactly one *$ref* in the list
and at most one *x-backref* in the list.

The other way, which is not recommended, adds the *x-backref* to the object
being referenced:

.. literalinclude:: ./relationships/many_to_one/backref_not_recommended.yaml
    :language: yaml
    :linenos:

The reason it is not recommended is because this only allows a *x-backref* per
table, whereas the other allows for many. If *x-backref* is both in the *allOf*
list and the referenced object, the value from the *allOf* list will be used.

Using *x-backref* is equivalent to the following traditional *models.py*:

.. literalinclude:: ../../../examples/relationship_many_to_one_backref_models_traditional.py
    :language: python
    :linenos:

.. seealso::
    :ref:`references` shows how to reference to other schemas.


.. _custom-foreign-key:

Custom Foreign Key
^^^^^^^^^^^^^^^^^^

The  *x-foreign-key-column* extension property is used to define a different
foreign key constraint column to the default *id* column. It is similar to the
:ref:`backref` extension property. There are two ways the foreign key constrain
can be defined. The first adds the *x-foreign-key-column* extension property
using *allOf* which allows for a different foreign key column for each
relationship:

.. literalinclude:: ./relationships/many_to_one/foreign_key_column_all_of.yaml
    :language: yaml
    :linenos:

The second adds the extension property on the referenced object:

.. literalinclude:: ./relationships/many_to_one/foreign_key_column_ref.yaml
    :language: yaml
    :linenos:

This allows for a common definition for the foreign key constraint for all
relationships referencing the same object. If *x-foreign-key-column* is both in
the *allOf* list and the referenced object, the value from the *allOf* list
will be used.

.. seealso::
    :ref:`foreign-key` describes how to define foreign key constraints.
