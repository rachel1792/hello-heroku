import os

import pytest

from xword.utils import auth
from app import app as _app
from app import db as _db


@pytest.fixture
def vcr_cassette_path(request, vcr_cassette_name):
    # Put all cassettes in vhs/{module}/{test}.yaml
    return os.path.join(
        'xword', 'tests', 'fixtures', 'vcr_cassettes',
        request.module.__name__.split('.')[-1], vcr_cassette_name.split('.')[-1]
    )


@pytest.fixture(scope='session', autouse=True)
def app(request):
    """Session-wide test `Flask` application."""
    _app.config['DEBUG'] = True
    _app.config['TESTING'] = True
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='function', autouse=True)
def db(app, request):
    """Test database."""
    _db.app = app
    _db.create_all()

    def teardown():
        _db.session.close_all()
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function', autouse=True)
def client(app):
    """Test client for the application."""
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def model_factory():
    """View model factory, to be overwritten for each view."""
    return None


@pytest.fixture(scope='function', autouse=True)
def model():
    """View model, to be overwritten for each view."""
    return None


@pytest.fixture(scope='function', autouse=True)
def url_prefix():
    """Url prefix, to be overwritten for each view."""
    return None


@pytest.mark.usefixtures('user')
@pytest.fixture(scope='function', autouse=True)
def token(user):
    """Generate an authentication token for the Domio user."""
    return auth.generate_token(user)


@pytest.fixture(scope='function', autouse=True)
def headers(token):
    return {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
