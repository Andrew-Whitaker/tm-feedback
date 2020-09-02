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
        self.url = reverse('performances:detail', kwargs={'perf_pk': self.performance.pk})
        self.response = self.client.get(self.url)

    def test_performance_detail_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_performance_detail_view_not_found_status_code(self):
        bad_url = reverse('performances:detail', kwargs={'perf_pk': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_perf_detail_view_contains_breadcrumb_links(self):
        # Page should have breadcrumb link back to their club home page
        club_home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # page should have breadcrumb link back to the meeting detail of that performance
        meeting_detail_url = reverse('meetings:detail', kwargs={'meeting_pk': self.meeting.pk})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_detail_url))

    def test_perf_detail_view_contains_eval_nav_links(self):
        # Should be a button to Evaluate
        create_eval_url = reverse('performances:create_eval', kwargs={'perf_pk': self.performance.pk})
        self.assertContains(self.response, 'href="{0}"'.format(create_eval_url))


class PerfDetailEditEvalButtonTests(TestCase):

    def test_edit_evaluation_button_only_appears_for_evaluator(self):
        self.assertTrue(False, 'TODO: Edit Eval button should only appear for original evaluator')

    def test_edit_evaluation_button_navigates_properly(self):
        self.assertTrue(False, 'TODO: Edit eval button should navigated to Eval edit page.')

