from django.db import models
from django.conf import settings


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='like_posts')

    def __str__(self):
        return f'{self.id}: {self.user}, {self.content[:30]}'
