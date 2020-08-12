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
            'club_id': self.club.id,
            'meeting_pk': self.meeting.pk,
            'perf_pk': self.performance.pk
        }
        self.url = reverse('eval_create', kwargs=url_path_kwargs)

    def test_eval_create_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_eval_create_view_not_found_status_code(self):
        bad_url = reverse('eval_create', kwargs={'club_id': self.club.id,
                                                 'meeting_pk': self.meeting.pk,
                                                 'perf_pk': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)
