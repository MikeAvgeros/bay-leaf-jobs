import os
if os.path.exists("env.py"):
    import env


class Config:
    """Base config variables for the app to run"""
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    """
    Config variables for production
    Extends base config variables
    """
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """
    Config variables during development
    Extends base config variables
    """
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


