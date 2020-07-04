from django.db import models
from django.conf import settings


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics',
                                   null=True, on_delete=models.SET_NULL)

    # def __str__(self):
    #     return self.subject[0:(min(15, len(self.subject) - 1))]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',
                                   null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+',
                                   on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    # def __str__(self):
    #     return self.message[0:(min(15, len(self.message) - 1))]
