import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from xword.utils.configuration import config


def configure_database(app):
    db.init_app(app)


def configure_sqlalchemy(app):
    database_url = os.environ.get('DATABASE_URL') or 'postgres://{}:{}@{}:{}/{}'.format(
        config.get('database.user'),
        config.get('database.password'),
        config.get('database.host'),
        config.get('database.port'),
        config.get('database.name'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5


def configure_app(app):
    """Create and initialize the application."""
    configure_sqlalchemy(app)
    configure_database(app)
    return app


db = SQLAlchemy()
app = Flask(__name__)
configure_app(app)
