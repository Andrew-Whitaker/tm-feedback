from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from clubs.models import Club
from meetings.models import Meeting, Performance
from ..models import Evaluation
from .test_eval_base import EvaluationTestBase


class EvalCreateViewTest(EvaluationTestBase):
    def setUp(self):
        super().setUp()
        self.client.login(username='john', password='12345678')
        url_path_kwargs = {
            'perf_pk': self.performance.pk
        }
        self.url = reverse('performances:create_eval', kwargs=url_path_kwargs)
        self.response = self.client.get(self.url)

    def test_eval_create_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_eval_create_view_not_found_status_code(self):
        bad_url = reverse('performances:create_eval', kwargs={'perf_pk': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_perf_detail_view_contains_breadcrumb_links(self):
        # Page should have breadcrumb link back to their club home page
        club_home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # page should have breadcrumb link back to the meeting detail of that performance
        meeting_detail_url = reverse('meetings:detail', kwargs={'meeting_pk': self.meeting.pk})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_detail_url))

        # page should have breadcrumb back to performance detail
        perf_detail_url = reverse('performances:detail', kwargs={'perf_pk': self.performance.pk})
        self.assertContains(self.response, 'href="{0}"'.format(perf_detail_url))
