from django.db import models
from django.conf import settings


class Club(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id_number = models.PositiveIntegerField(unique=True, default=0)
    summary = models.TextField(max_length=1000)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clubs')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organizing',
                                  null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
