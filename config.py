import os
if os.path.exists("env.py"):
    import env


class Config:
    """Base config variables for the app to run"""
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
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


