from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from datetime import timedelta

from ..models import Club
from meetings.models import Meeting


class ClubFindMeetingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='john', password='12345678')
        self.club = Club.objects.create(name='Club', id=1, description='', organizer=self.user, member_count=1)

        # create meetings
        date_i = date(2020, 6, 30)
        delta_week = timedelta(days=7)
        for i in range(8):
            Meeting.objects.create(date=date_i, theme='Theme {}'.format(i), club=self.club)
            date_i = date_i + delta_week

    def test_get_meetings_in(self):
        # Get meetings from month with no meetings
        q_set = self.club.get_meetings_in(6, 2019)
        self.assertFalse(q_set.exists())

        # Get Meetings from June
        q_set = self.club.get_meetings_in(6, 2020)
        self.assertEquals(q_set.count(), 1)

        # Get Meetings from July
        q_set = self.club.get_meetings_in(7, 2020)
        self.assertEquals(q_set.count(), 4)

        # Get Meetings from August
        q_set = self.club.get_meetings_in(8, 2020)
        self.assertEquals(q_set.count(), 3)

    def test_get_meetings_from_past_n_months_success(self):
        #
        today = date(2020, 8, 17)
        # Get meetings from past 1 week including today
        q_set = self.club.get_meetings_from_last_n_weeks(1, date=today)
        self.assertEquals(q_set.count(), 1)

        # Get meetings from past 3 weeks
        q_set = self.club.get_meetings_from_last_n_weeks(3, date=today)
        self.assertEquals(q_set.count(), 3)

        # Get meetings from past 8 weeks
        q_set = self.club.get_meetings_from_last_n_weeks(8, date=today)
        self.assertEquals(q_set.count(), 7)


