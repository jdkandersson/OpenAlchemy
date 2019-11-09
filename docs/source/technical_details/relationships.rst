.. _relationship:

Defining Relationships
======================

Defining relationships between tables is done by using *$ref* to reference
other objects from an object property.

.. seealso::

   `SQLAlchemy relationship documentation <https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html>`_
      Documentation for SQLAlchemy relationships.

.. _many-to-one:

Many to One
-----------

A many to one relationship associates many children with a single parent. For
example, a company can have many employees working in the same division (for
example engineering, legal, marketing, ...) but a particular employee can only
work in one division. In this case the employees are the children on the "many"
side and the division is the parent on the "one" side. The following *OpenAPI*
specification snippet defines a many to one relationship:

.. literalinclude:: ./relationships/many_to_one/example.yaml
    :language: yaml
    :linenos:

By adding a *$ref* to an object property that points at another object, a
relationship with the logical name will be formed. For example, if the *$ref*
points to the *Division* object, *sqlalchemy.orm.relationship* with
*"Division"* will be called.

Alongside the *relationship*, a foreign key will also be added to the table
with the *$ref* property under the name of the property suffixed with *_id*.
Note that, the object being referenced must have the *id* property.

The only way to make the foreign key column not nullable is to add the
property with the reference to the *required* list. For example:

.. literalinclude:: ./relationships/many_to_one/example-required.yaml
    :language: yaml
    :linenos:

OpenAlchemy defined relationships are equivalent to the following traditional
*models.py*:

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

.. _one-to-one:

One to One
----------

A one to one relationship associates one child with one parent and vice-versa.
For example, the pay information for an employee may be stored in a different
table than the employee. However, one employee can only be paid one one way
and each employee must be paid separately. This means that there is a one to
one relationship between an employee and pay information.

The one to one relationship is defined in the same way as the
:ref:`many to one <many-to-one>` relationship except that it requires the
*x-uselist* extension property to be set to *False* and
:ref:`x-backref <backref>` to be defined.
:ref:`Custom foreign keys <custom-foreign-key>` are also supported. The
*x-uselist* property can be defined along with the *x-backref* extension
property using *allOf* or on the object being referenced. To define it on
*allOf*:

.. literalinclude:: ./relationships/one_to_one/example_recommended.yaml
    :language: yaml
    :linenos:

This is the recommended approach as it allows for other relationships to the
referenced object to be, for example, many to one relationships. To default
relationships to an object to one to one, the *x-uselist* property can be set
on the referenced object:

.. literalinclude:: ./relationships/one_to_one/example_not_recommended.yaml
    :language: yaml
    :linenos:

If *x-uselist* is both in  the *allOf* list and the referenced object, the
value from the *allOf* list will be used. The *x-uselist* and *x-backref*
properties don't have to be defined together, they can be separated. For
example:

.. literalinclude:: ./relationships/one_to_one/uselist-backref-separated.yaml
    :language: yaml
    :linenos:

Other permutations are also supported.
