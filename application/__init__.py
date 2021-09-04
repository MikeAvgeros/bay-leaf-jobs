from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail


# Instantiate PyMongo and Mail
mongo = PyMongo()
mail = Mail()


def create_app():
    """Initialize the application."""
    app = Flask(__name__, instance_relative_config=False)


    # Configure the application instance using the Config class
    app.config.from_object('config.DevConfig')


    # Setup an instance of PyMongo and Mail
    mongo.init_app(app)
    mail.init_app(app)


    # Import and register Blueprints
    from application.main.routes import main
    from application.users.routes import users
    from application.jobs.routes import jobs


    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(jobs)


    return app
