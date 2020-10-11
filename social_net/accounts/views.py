import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
)
from django.views.decorators.csrf import csrf_exempt

from .third_party_requests import (
    verify_email,
    fetch_data_on_email,
)
from .tokens import get_token


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(View):
    def post(self, request):
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token = get_token(request.session, user)
            return JsonResponse({'token': token}, status=200)
        return JsonResponse({'error': 'something went wrong'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class SignupAPI(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            username = body['username']
            email = body['email']
            password = body['password']
            if verify_email(email):
                data = fetch_data_on_email(email)
                user_model = get_user_model()
                user_model.objects.create_user(username,
                                               email,
                                               password,
                                               first_name=data['first_name'],
                                               last_name=data['last_name'])
                return JsonResponse({
                    'username': username,
                    'email': email,
                    'user_id': user.id
                }, status=201)
            else:
                return JsonResponse({'error': 'email is not verifiable'})
        except KeyError:
            return JsonResponse({
                'error': 'you must supply username, email and password'
            }, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'this user is already registered'})
