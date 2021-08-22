from flask import Flask
from flask_pymongo import PyMongo


# Instantiate PyMongo
mongo = PyMongo()


def init_app():
    """Initialize the application."""
    app = Flask(__name__, instance_relative_config=False)


    # Configure the application instance using the Config class
    app.config.from_object('config.DevConfig')


    # Setup an instance of PyMongo
    mongo.init_app(app)


    # Import and register Blueprints
    from application.main.routes import main
    from application.users.routes import users


    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)


    return app
