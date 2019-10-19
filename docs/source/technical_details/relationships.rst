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

.. literalinclude:: ../../../examples/relationship-example-spec.yml

By adding a *$ref* to an object property that points at another object, a
relationship with the logical name will be formed. For example, if the *$ref*
points to the *Division* object, *sqlalchemy.orm.relationship* with
*"Division"* will be called. Note that you must add both objects to the
*models.py* file. For example:

.. literalinclude:: ../../../examples/relationship_models.py

Alongside the *relationship*, a foreign key will also be added to the table
with the *$ref* property under the name of the property suffixed with *_id*.
Note that, the object being referenced must have the *id* property.

The only way to make the foreign key column not nullable is to add the
property with the reference to the *required* list.

Without OpenAPI-SQLAlchemy, the following is the equivalent *models.py* file:

.. literalinclude:: ../../../examples/relationship_models_traditional.py

Backref
^^^^^^^

One of the features of *SQLAlchemy* is that a relationship can be back
populated to the referred table. This is supported using the *x-backref*
key. There are 2 places where the *x-backref* key can be defined. The
recommended implementation adds it using *allOf*:

.. literalinclude:: ./relationships/many_to_one/backref_recommended.yaml

Note that, when *allOf* is used, there must be exacly one *$ref* in the list
and at most one *x-backref* in the list.

The other way, which is not recommended, adds the *x-backref* to the object
being referenced:

.. literalinclude:: ./relationships/many_to_one/backref_not_recommended.yaml

The reason it is not recommended is because this only allows a *x-backref* per
table, whereas the other allows for many.

.. seealso::
    :ref:`references` shows how to reference to other schemas.
