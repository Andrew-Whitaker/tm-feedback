from django.db import models
from django.conf import settings
from datetime import date as dt
from django.shortcuts import reverse

from clubs.models import Club


class Meeting(models.Model):
    date = models.DateField()
    theme = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='meetings')

    def __str__(self):
        return self.theme + ' - ' + dt.strftime(self.date, "%b %d, %Y")

    def get_absolute_url(self):
        kwargs = {
            'club_id': self.club.id,
            'meeting_pk': self.pk
        }
        return reverse('meeting_detail', kwargs=kwargs)


