# Alembic Interoperability

The following steps were used to generate the migration.

1. Run `alembic init alembic`
2. Modify [alemnbic.ini](alembic.ini) `driver://user:pass@localhost/dbname`
   to `sqlite:///:memory:` to use an in-memory SQLite database.
3. Modify [env.py](alembic/env.py) by adding `import open_alchemy` at the
   bottom of the import section and
   `open_alchemy.init_yaml(spec_filename="../app/api.yaml")` below that to load
   the SQLAlchemy models for the example [app](../app).
4. Modify [env.py](alembic/env.py) by changing `target_metadata = None` to
   `target_metadata = open_alchemy.models.Base.metadata`
5. Run `alembic revision --autogenerate -m "Add emplpoyee table"` to generate
   the [revision](alembic/versions)
