from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Meeting, Performance
from clubs.models import Club


class PerformanceDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com')
        self.user.set_password('12345678')
        self.user.save()
        self.client.login(username='john', password='12345678')
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=self.user)
        self.meeting = Meeting.objects.create(date='2020-07-28', theme='Test Theme', club=self.club)
        self.performance = Performance.objects.create(meeting=self.meeting, performer=self.user,
                                                      role=Performance.Role.SPEAKER)
        self.url = reverse('performance_detail', kwargs={'club_id': self.club.id,
                                                         'meeting_pk': self.meeting.pk,
                                                         'perf_pk': self.performance.pk})

    def test_performance_detail_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_performance_detail_view_not_found_status_code(self):
        bad_url = reverse('performance_detail', kwargs={'club_id': self.club.id,
                                                        'meeting_pk': self.meeting.pk,
                                                        'perf_pk': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)


