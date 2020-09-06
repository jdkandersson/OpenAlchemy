"""Application code."""

import connexion
import database

# Creating Flask app
app = connexion.FlaskApp(__name__, specification_dir=".")

# Initializing database
app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
database.db.init_app(app.app)
with app.app.app_context():
    database.db.create_all()

# Running app
app.add_api("api.yaml")
app.run(port=8080)
