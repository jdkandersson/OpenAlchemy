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
work in one division. In this case the employees are the parents on the "many"
side and the division is the child on the "one" side. The following *OpenAPI*
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

.. _many-to-one-nullable:

Nullable
^^^^^^^^

Similar to simple value columns (such as *integer*), many to one relationships
are also nullable. This is supported using the *nullable* key or by including
the property in the *required* array of the schema. There are 2 places where
the *nullable* key can be defined. The recommended implementation adds it using
*allOf*:

.. literalinclude:: ./relationships/many_to_one/nullable_recommended.yaml
    :language: yaml
    :linenos:

Note that, when *allOf* is used, there must be exactly one *$ref* in the list
and at most one *nullable* in the list.

The other way, which is not recommended, adds *nullable* to the object being
referenced:

.. literalinclude:: ./relationships/many_to_one/nullable_not_recommended.yaml
    :language: yaml
    :linenos:

The reason it is not recommended is because this only allows a *nullable* per
table, whereas the other allows for many. Also, some relationships do not
support *nullable* which means an error is raised when that type of
relationship refers to the same schema. If *nullable* is both in the *allOf*
list and the referenced object, the value from the *allOf* list will be used.

The following example makes the relationship not nullable using the required
array:

.. literalinclude:: ./relationships/many_to_one/nullable_required.yaml
    :language: yaml
    :linenos:

Note that if you use both the nullable and required method, nullable takes
precedence over required.

Setting *nullable* to *false* is equivalent to the following traditional
*models.py*:

.. literalinclude:: ../../../examples/relationship_many_to_one_not_nullable_models_traditional.py
    :language: python
    :linenos:

.. seealso::
    :ref:`null` shows how nullable works for simple values such as integers.

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

It is also possible to define a property with the name that would otherwise be
automatically generated by *OpenAlchemy* to have more control over how the
foreign key property is defined. For example:

.. literalinclude:: ./relationships/many_to_one/foreign_key_property_defined.yaml
    :language: yaml
    :linenos:

Note the following:

* When *OpenAlchemy* constructs the foreign key for you, the name of the
  property is made up of the name of the property referencing the object
  (*division* in the previous example) combined with the name of the property
  in the foreign key constraint (*id* in the previous example). These two
  values are combined as follows:
  "<reference property name>_<foreign key column name>" (*division_id* in the
  previous example).
* If *OpenAlchemy* finds that property in the schema, it won't construct a
  foreign key property automatically.
* The defined property is type checked against the expected foreign key type
  based on the relationship.
* The defined property is checked for the *x-foreign-key* property against the
  expected foreign key constraint based on the relationship.
* The *x-foreign-key-column* extension property can be used to control which
  property is used as the foreign key.
* When the foreign key is defined, the *from_dict* and *to_dict* model
  functions will use/return the foreign key values.

.. seealso::
    * :ref:`foreign-key` describes how to define foreign key constraints.
    * :ref:`from-dict` describes how to convert dictionaries to model instances.
    * :ref:`to-dict` describes how to convert model instances to dictionaries.

.. _one-to-one:

One to One
----------

A one to one relationship associates one child with one parent and vice-versa.
For example, the pay information for an employee may be stored in a different
table than the employee. However, one employee can only be paid in one way
and each employee must be paid separately. This means that there is a one to
one relationship between an employee and pay information.

The one to one relationship is defined in the same way as the
:ref:`many to one <many-to-one>` relationship except that it requires the
*x-uselist* extension property to be set to *False* and
:ref:`x-backref <backref>` to be defined.
:ref:`Custom foreign keys <custom-foreign-key>` and
:ref:`nullable <many-to-one-nullable>` are also supported. The *x-uselist*
property can be defined along with the *x-backref* extension property using
*allOf* or on the object being referenced. To define it on *allOf*:

.. literalinclude:: ./relationships/one_to_one/example_recommended.yaml
    :language: yaml
    :linenos:

This is the recommended approach as it allows for other relationships to the
referenced object to be, for example, many to one relationships. For some types
of relationships the inclusion of *x-uselist* causes an error to be raised. To
default relationships to an object to one to one, the *x-uselist* property can
be set on the referenced object:

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

.. _one-to-many:

One to Many
-----------

The one to many relationship is similar to the may to one relationship except
that the role of the child and parent is swapped. Following on from the
:ref:`many to one <many-to-one>` example, in the one to many case the division
would be the parent and the employees the children. The following *OpenAPI*
specification snippet defines a one to many relationship:

.. literalinclude:: ./relationships/one_to_many/example.yaml
    :language: yaml
    :linenos:

The one to many relationship also supports back references and custom foreign
keys. They are defined similar to how they are defined for many to one
relationships. For back references see :ref:`many to one backref <backref>`
and for custom foreign keys see
:ref:`many to one custom foreign keys <custom-foreign-key>`. Note that
*x-uselist* is not supported as it does not make sense to turn a one to many
relationship defined as an OpenAPI array into a one to one relationship. Also
note that :ref:`nullable <many-to-one-nullable>` is not supported because the
foreign key is defined on the referenced schema. If the foreign key was not
nullable by default, then that schema cannot be constructed without the foreign
key. If you need to define a foreign key that is not nullable, add it as a
property on the referenced schema and refer to that property using
:ref:`many to one custom foreign keys <custom-foreign-key>`.

.. _dict-ignore:

.. note:: To be able to support one to many relationships, the schemas stored
    with the model factory may be modified by putting a particular schema
    behind an *allOf* statement together with a object that has a foreign key
    property. The schema for the added object will include the *x-dict-ignore*
    extension property to ensure that *from_dict* and *to_dict* don't attempt
    to construct the foreign key associated with the one to many relationship.
    The *x-dict-ignore* extension property is an internal extension property
    that may change at any time and should not be used externally.

.. _many-to-many:

Many to Many
------------

The many to many relationship is used when a parent model can have many
children but the child can also have many parents. For example, an employee
could be working on multiple projects and multiple employees are generally
assigned to a project. Therefore, there is a many to many relationship between
employees and projects. This is implemented using an association table which
has a column for each primary key on the parent and child. One row in the
association table implies a relationship between the parent and child.

Many to many relationships are defined similar to
:ref:`one to many <one-to-many>` relationships except that the *x-secondary*
extension property is required to define the name of the association table.
Both the parent and child must have a primary key column and, currently, both
the parent and child must only have one primary key column. In the presence of
the *x-secondary* extension property, a table with the name as the property
value is constructed where the columns are defined based on the schema of the
primary key columns of the parent and child. The names of the columns are
defined to be "\<*x-tablename*>_\<property name>". Each column is given a
foreign key constraint as defined by "\<*x-tablename*>.\<property name>".

There are 2 places where the *x-secondary* key
can be defined. The recommended implementation adds it using *allOf*:

.. literalinclude:: ./relationships/many_to_many/example_recommended.yaml
    :language: yaml
    :linenos:

Note that, when *allOf* is used, there must be exactly one *$ref* in the list
and at most one *x-secondary* in the list. The other way, which is not
recommended, adds the *x-secondary* to the object being referenced:

.. literalinclude:: ./relationships/many_to_many/example_not_recommended.yaml
    :language: yaml
    :linenos:

The reason it is not recommended is because this only allows a *x-secondary*
per table, whereas the other allows for many. If *x-secondary* is both in the
*allOf* list and the referenced object, the value from the *allOf* list will be
used.

Using *x-secondary* is equivalent to the following traditional *models.py*:

.. literalinclude:: ../../../examples/relationship/many_to_many/models_traditional.py
    :language: python
    :linenos:

Many to many relationships support *x-backref*, see
:ref:`many to one backref <backref>`. Note that *x-uselist* is not supported as
it does not make sense to turn a many to many relationship defined as an
OpenAPI array into a many to one relationship. Also, because the association
table is defined based on the primary key properties, custom foreign keys are
not supported.

.. _child-parent-reference:

Including Parent References with Child
--------------------------------------

So far, relationships have been used to include the full details for a child
with a parent. This is only possible from one side of the relationship without
circular references that would produce infinite sized API response payloads.
This can be overcome by including a subset of parent properties in the child.

This is done using *readOnly* properties. At a high level, properties marked as
*readOnly* are not constructed as columns in the *SQLAlchemy* models. They are
also not constructed as a part of a call to *from_dict*. The purpose of
*readOnly* properties is to include some of the properties of the parent in the
child dictionary when calling *to_dict*. *readOnly* properties are required to
be defined as objects or arrays of object. In both cases object properties may
not be of type object nor array to avoid circular references. *$ref* and
*allOf* are supported as normal.

Many to One
^^^^^^^^^^^

For example, the following *Division* schema includes the *id* of all employees
working in the division as an array:

.. literalinclude:: ./relationships/many_to_one/read-only.yaml
    :language: yaml
    :linenos:

Querying for a *Division* would, for example, result in the following
dictionary::

    >>> division = Division.query.first()
    >>> division.to_dict()
    {'id': 1, 'name': 'Engineering', 'employees': [{'id': 1}, {'id': 2}, ['id': 5}]}

Indicating that employees with the ids *1*, *2* and *5* work in the
engineering division. To retrieve further details for those employees, the
relevant endpoints can be queried with the ids.

Any number of properties may be included in the *readOnly* object schema.
Schema duplication can be reduced by making use of *$ref*. For example:

.. literalinclude:: ./relationships/many_to_one/read-only-$ref.yaml
    :language: yaml
    :linenos:

This means that all *Employee* properties are included except for the reference
to *Division* to avoid circular references.

In the above example, there is a many to one relationship from *Employee* to
*Division*. The difference for other relationship types is the type of the
*readOnly* property.

One to One
^^^^^^^^^^

The difference between many to one and one to one is that the type of the
*readOnly* property is an object instead of an array.

.. literalinclude:: ./relationships/one_to_one/read-only.yaml
    :language: yaml
    :linenos:

Querying for a *PayInfo* would, for example, result in the following
dictionary::

    >>> pay_info = PayInfo.query.first()
    >>> pay_info.to_dict()
    {'id': 1, 'account': '012 345', 'employee': {'id': 1}}

Indicating that the pay information is for the employee with an id of *1*.


One to Many
^^^^^^^^^^^

Including a parent reference with a child for a one to many relationship is
very similar to the one to one relationship case. To illustrate, the following
schema redefines the relationship between *Employee* and *Division* so that the
*Division* is the parent resulting in a one to many relationship:

.. literalinclude:: ./relationships/one_to_many/read-only.yaml
    :language: yaml
    :linenos:

Querying for an *Employee* would, for example, result in the following
dictionary::

    >>> employee = Employee.query.first()
    >>> employee.to_dict()
    {'id': 1, 'name': 'David Andersson', 'division': {'id': 1}}

Indicating that the employee is working in the division with an id of *1*.


Many to Many
^^^^^^^^^^^^

Including a parent reference with a child for a many to many relationship is
very similar to the many to one relationship case except that both sides are
defined as arrays. To illustrate, the following schema defines a many to many
relationship between *Employee* and *Project*:

.. literalinclude:: ./relationships/many_to_many/read-only.yaml
    :language: yaml
    :linenos:

Querying for an *Employee* would, for example, result in the following
dictionary::

    >>> employee = Employee.query.first()
    >>> employee.to_dict()
    {'id': 1, 'name': 'David Andersson', 'projects': [{'id': 1}, {'id': 2}]}

Indicating that the employee is working on the projects with an id of *1* and
*2*. Querying for a *Project* would, for example, result in the following
dictionary::

    >>> project = Project.query.first()
    >>> project.to_dict()
    {'id': 1, 'name': 'Expand to the USA', 'employees': [{'id': 1}, {'id': 3}]}

Indicating that the project is being worked on by the employees with an id of
*1* and *3*.
