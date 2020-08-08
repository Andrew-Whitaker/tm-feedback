from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def get_deleted_default_user():
        (user, created) = User.objects.get_or_create(
            first_name='Deleted',
            last_name='User',
            username='deleted_user'
        )
        return user
