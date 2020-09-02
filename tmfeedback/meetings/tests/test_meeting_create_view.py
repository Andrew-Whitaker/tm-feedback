from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import MeetingCreateView
from ..models import Meeting
from clubs.models import Club


class MeetingCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='john', email='john@doe.com')
        self.user.set_password('1234')
        self.user.save()
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=self.user)
        self.club.add_member(self.user)

        login = self.client.login(username='john', password='1234')
        self.url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        self.response = self.client.get(self.url)

    def test_meeting_create_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_meeting_create_view_not_found_status_code(self):
        bad_url = reverse('clubs:create_meeting', kwargs={'club_id': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_meeting_create_url_resolves_create_view(self):
        view = resolve('/clubs/{}/meetings/create/'.format(self.club.id))
        self.assertEquals(view.func.view_class, MeetingCreateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_meeting_create_view_contains_breadcrumb_links(self):
        # User should have breadcrumb link back to their club home page
        club_home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # User should have breadcrumb link back to the meeting list of that club
        meeting_list_url = reverse('clubs:meeting_index', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{}"'.format(meeting_list_url))

    def test_create_meeting_valid_post_data(self):
        url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        data = {
            'date': '2020-07-28',
            'theme': 'Test Theme'
        }
        response = self.client.post(url, data)
        # TODO: figure out why response.context is Nonetype in this test
        #  but not in the invalid_data test below
        # form = response.context['form']
        # self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Meeting.objects.exists(),
                        'The club did not get created')
        meeting = Meeting.objects.get(pk=1)
        self.assertEquals(meeting.theme, 'Test Theme')

    def test_create_meeting_invalid_post_data(self):
        url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)


class MeetingCreateViewPermissionRequirementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='john', email='john@doe.com')
        self.user.set_password('1234')
        self.user.save()
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=self.user)

    def test_unauthenticated_redirection(self):
        url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

    def test_non_club_member_forbidden_access(self):
        login = self.client.login(username='john', password='1234')
        url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_club_member_access(self):
        self.club.add_member(self.user)
        login = self.client.login(username='john', password='1234')
        url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class MeetingCreationFunctionalityTests(TestCase):

    def test_no_duplicate_meetings(self):
        self.assertTrue(False, "TODO: Have not enforced no duplicate meeting creations.")



