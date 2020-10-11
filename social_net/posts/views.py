import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Post

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@method_decorator(csrf_exempt, name='dispatch')
class PostAPI(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            body = json.loads(request.body)
            content = body['content']
            post = Post(user=user, content=content)
            post.save()
            return JsonResponse({
                'id': post.id,
                'content': post.content,
                'user': {
                    'id': post.user.id,
                    'username': post.user.username,
                },
            }, status=201)
        except KeyError:
            logger.error('check')
            return JsonResponse({
                'error': 'content must be a key on the json body of the request'
            }, status=400)
        except Exception as e:
            logger.error(f'{e}')
            return JsonResponse({
                'error': str(e)
            })


@method_decorator(csrf_exempt, name='dispatch')
class PostInfoAPI(LoginRequiredMixin, View):
    def patch(self, request, post_id):
        body = json.loads(request.body)
        try:
            like = body['like']
            user = request.user
            post = Post.objects.get(pk=post_id)
            if post.user.id == user.id:
                return JsonResponse({
                    'error': "user can't like his own posts"
                }, status=400)

            if like.lower() == 'like':
                post.like.add(user)
            elif like.lower() == 'unlike':
                post.like.remove(user)
            else:
                return JsonResponse({
                    'error': 'like must be either like or unlike'
                }, status=400)

            post.save()
            return JsonResponse({
                'success': True
            }, status=200)
        except KeyError:
            return JsonResponse({
                'error': 'like must be a key on the json body of the request'
            }, status=400)
