from django.db import models
from django.conf import settings
from datetime import date as dt
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from clubs.models import Club


class Meeting(models.Model):
    date = models.DateField()
    theme = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='meetings')

    def __str__(self):
        return dt.strftime(self.date, "%b %d, %Y") + ' - ' + self.theme

    def get_absolute_url(self):
        kwargs = {
            'club_id': self.club.id,
            'meeting_pk': self.pk
        }
        return reverse('meeting_detail', kwargs=kwargs)


def get_default_user():
    return get_user_model().get_deleted_default_user()


class Performance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='performances')
    performer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET(get_default_user),
                                  related_name='performances')

    # Performance Roles
    class Role(models.TextChoices):
        TOASTMASTER = 'TMD', _('Toastmaster')
        TABLE_TOPICS_MASTER = 'TTM', _('Table Topics Master')
        EVALUATOR = 'EVAL', _('Evaluator')
        GENERAL_EVALUATOR = 'GE', _('General Evaluator')
        SPEAKER = 'S', _('Speaker')
        TABLE_TOPICS_SPEAKER = 'TTS', _('Table Topics Speaker')

    role = models.CharField(max_length=4, choices=Role.choices, default=Role.SPEAKER)

    def __str__(self):
        return '{date} {role} {user}'.format(date=dt.strftime(self.meeting.date, "%m-%d-%y"),
                                             role=self.get_role_label(),
                                             user=self.performer.first_name)

    def get_role_label(self):
        return self.Role(self.role).label

