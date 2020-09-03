from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from clubs.models import Club
from meetings.models import Meeting, Performance
from ..models import Evaluation
from ..views import EvalCreateView
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

    def test_eval_create_url_resolves_view(self):
        view = resolve('/performances/{0}/evals/create/'.format(self.performance.pk))
        self.assertEquals(view.func.view_class, EvalCreateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

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

    def test_create_eval_valid_post_data(self):
        data = {
            'you_excelled_at': 'Good things',
            'to_work_on': 'bad things',
            'challenge_yourself_by': 'uncomfortable things'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Evaluation.objects.exists(), 'The eval did not get created')
        eval = Evaluation.objects.get(pk=1)
        self.assertEquals(eval.to_work_on, 'bad things')

    def test_create_eval_invalid_post_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)


class EvalCreateViewPermissionRequirementTests(EvaluationTestBase):
    def setUp(self):
        super().setUp()
        url_path_kwargs = {
            'perf_pk': self.performance.pk
        }
        self.url = reverse('performances:create_eval', kwargs=url_path_kwargs)

    def test_unauthenticated_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

    def test_non_club_member_forbidden_access(self):
        self.user = get_user_model().objects.create_user(username='jane', email='jane@doe.com')
        self.user.set_password('12345678')
        self.user.save()
        self.client.login(username='jane', password='12345678')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 403)

    def test_club_member_access(self):
        self.client.login(username='john', password='12345678')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

