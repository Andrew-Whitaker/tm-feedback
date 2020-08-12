from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from clubs.models import Club
from meetings.models import Meeting, Performance
from ..models import Evaluation


class EvaluationTestBase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com')
        self.user.set_password('12345678')
        self.user.save()
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=self.user)
        self.meeting = Meeting.objects.create(date='2020-07-28', theme='Test Theme', club=self.club)
        self.performance = Performance.objects.create(meeting=self.meeting, performer=self.user,
                                                      role=Performance.Role.SPEAKER)
