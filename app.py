import os

from flask import Flask

from xword.lib.database import db
from xword.models import *  # NOQA Import all the models, very important
from routes import simple_page
from xword.utils.configuration import config


app = Flask(__name__)
database_url = os.environ.get('DATABASE_URL') or 'postgres://{}:{}@{}:{}/{}'.format(
    config.get('database.user'),
    config.get('database.password'),
    config.get('database.host'),
    config.get('database.port'),
    config.get('database.name'),
)

# app.secret_key = config.get('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(simple_page)


if __name__ == '__main__':
    app.run()
