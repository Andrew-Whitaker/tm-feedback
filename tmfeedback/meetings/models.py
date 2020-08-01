from django.db import models
from django.conf import settings
from datetime import date as dt

from clubs.models import Club


class Meeting(models.Model):
    date = models.DateField()
    theme = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='meetings')

    def __str__(self):
        return dt.strftime(self.date, "%b %d, %Y")

