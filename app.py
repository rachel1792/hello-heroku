import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import Xwords


def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            print('thanks for the request!')
        except Exception:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()
