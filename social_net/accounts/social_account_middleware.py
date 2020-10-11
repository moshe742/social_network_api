from django.conf import settings

from .tokens import get_session_key


class SocialAccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        authorization = request.headers.get('Authorization')
        if authorization:
            request.COOKIES[settings.SESSION_COOKIE_NAME] = get_session_key(authorization)

        response = self.get_response(request)

        return response
