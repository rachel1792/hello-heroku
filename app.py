import os

from flask import Flask

from xword.lib.database import db
from routes import simple_page


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(simple_page)


if __name__ == '__main__':
    app.run()