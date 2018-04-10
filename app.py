from xword import app
from xword.utils.configuration import config


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=config.get('debug'), port=config.get('port'), threaded=True)
