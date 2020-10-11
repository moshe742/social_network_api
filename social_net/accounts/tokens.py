import jwt

from django.conf import settings


def get_token(session, user):
    token = jwt.encode({'user_id': user.id, 'session_key': session.session_key}, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def get_session_key(token):
    data = jwt.decode(token, settings.SECRET_KEY)
    return data['session_key']
