import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

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


class Xwords(db.Model):
    __tablename__ = 'xwords'

    id = sa.Column(UUID, default=lambda: uuid4().hex, primary_key=True)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        default=sa.func.now(),
        nullable=False
    )
    clue = sa.Column(sa.String(30), nullable=False)
    answer = sa.Column(sa.String(150), nullable=False)
    debut = sa.Column(sa.Boolean(), default=sa.false(), server_default=sa.false())
    unique = sa.Column(sa.Boolean(), default=sa.false(), server_default=sa.false())
