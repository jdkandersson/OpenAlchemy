connexion
=========

connexion is a package that allows you to define Flask APIs and how endpoints
are fulfilled using an OpenAPI specification. This has the advantage that a UI
is automatically generated and data that is passed to endpoints is validated
based on the OpenAPI specification. By combining connexion with
OpenAPI-SQLAlchemy, the OpenAPI specification not only defines the Flask
application but also the SQLALchemy models.

.. contents::
    :depth: 2

.. seealso::

   `connexion documentation <https://connexion.readthedocs.io/en/latest/>`_
      Documentation for connexion.

API specification
-----------------

As the case for combining connexion with OpenAPI-SQLAlchemy is compelling, an
example application has been included here. The API is designed to keep track
of employees of a company. The OpenAPI specification is:

.. literalinclude:: ../../../examples/app/api.yaml

There is a *POST* endpoint for inserting new employees into the database, a
*GET* endpoint for all employees and for a specific employee by id, there is a
*PATCH* endpoint for updating an employee and a *DELETE* endpoint for deleting
an employee.

Database Models
---------------

The OpenAPI specification above includes a *schemas* section which defines the
*Employee* schema. This schema is used to construct the *Employee* model. The
database setup is defined in the following file:

.. literalinclude:: ../../../examples/app/database.py

Endpoint Fulfillment
--------------------

The API endpoints are all fulfilled in the *api.py* file which has a function
for each combination of path and method:

.. literalinclude:: ../../../examples/app/api.py

App Construction
----------------

All the steps needed to make the Flask app work are defined in the *app.py*
file:

.. literalinclude:: ../../../examples/app/app.py

Conclusion
----------

The duplication of the data schema has been reduced by defining the SQLAlchemy
models based on the OpenAPI specification. This means that, to change the
database schema, the OpenAPI specification has to be updated and vice-versa.
This ensures that the two are always in synch and up to date.
