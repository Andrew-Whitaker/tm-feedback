from django.db import models
from django.conf import settings


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    id = models.PositiveIntegerField(default=0, primary_key=True)
    description = models.TextField(max_length=1500, default='')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clubs')
    member_count = models.PositiveIntegerField(default=1)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organizing',
                                  null=True, on_delete=models.SET_NULL)
    membership_requests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pending_clubs')

    def __str__(self):
        return self.name

    def has_member(self, user):
        return self.members.filter(pk=user.pk).exists()

    def has_pending_member(self, user):
        return self.membership_requests.filter(pk=user.pk).exists()
