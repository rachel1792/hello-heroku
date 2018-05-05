from functools import wraps

from flask import request, g, jsonify
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import app

ONE_WEEK = 604800


def generate_token(user, expiration=ONE_WEEK):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'id': user.id,
        'email': user.email,
    }).decode('utf-8')
    return token


def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # exempt from auth
        if request.method == 'POST' and '/api/v1/users' in request.path:
            return f(*args, **kwargs)
        if request.method == 'GET' and '/listings' in request.full_path:
            return f(*args, **kwargs)
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode(
                'ascii', 'ignore').replace('Bearer ', '')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

        return jsonify(message='Authentication is required to access this resource'), 401

    return decorated
