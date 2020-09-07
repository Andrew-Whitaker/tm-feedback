from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import Truncator

from meetings.models import Performance


def get_default_user():
    return get_user_model().get_deleted_default_user()


class Evaluation(models.Model):
    you_excelled_at = models.TextField(max_length=1000, default='')
    to_work_on = models.TextField(max_length=1000, default='')
    challenge_yourself_by = models.TextField(max_length=1000, default='')
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='evals_received')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET(get_default_user),
                                  related_name='evals_given')

    def __str__(self):
        evaluation = {
            'pk': self.pk,
            'evaluator': self.evaluator,
            'performer': self.performance.performer
        }
        return 'E{pk}: {evaluator} -> {performer}'.format(**evaluation)

    def get_absolute_url(self):
        meeting = self.performance.meeting
        club = meeting.club
        kwargs = {
            'perf_pk': self.performance.pk
        }
        return reverse('performances:detail', kwargs=kwargs)

    def get_general_comments(self):
        general_comments = [('You excelled at', self.you_excelled_at),
                            ('To work on', self.to_work_on),
                            ('Challenge yourself by', self.challenge_yourself_by)]
        return general_comments


