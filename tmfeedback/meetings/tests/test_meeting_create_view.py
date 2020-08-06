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
        self.url = reverse('meeting_create', kwargs={'club_id': self.club.id})
        self.response = self.client.get(self.url)

    def test_meeting_create_view_success_status_code(self):

        self.assertEquals(self.response.status_code, 200)

    def test_meeting_create_view_not_found_status_code(self):
        bad_url = reverse('meeting_create', kwargs={'club_id': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_meeting_create_url_resolves_create_view(self):
        view = resolve('/clubs/{}/meetings/create/'.format(self.club.id))
        self.assertEquals(view.func.view_class, MeetingCreateView)

    def test_meeting_create_view_contains_breadcrumb_links(self):
        # User should have breadcrumb link back to their club home page
        club_home_url = reverse('club_home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # User should have breadcrumb link back to the meeting list of that club
        meeting_list_url = reverse('meeting_list', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{}"'.format(meeting_list_url))


class MeetingCreateViewUserRequirementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='john', email='john@doe.com')
        self.user.set_password('1234')
        self.user.save()
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=self.user)

    def test_unauthenticated_redirection(self):
        url = reverse('meeting_create', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

    def test_non_club_member_forbidden_access(self):
        login = self.client.login(username='john', password='1234')
        url = reverse('meeting_create', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_club_member_access(self):
        self.club.add_member(self.user)
        login = self.client.login(username='john', password='1234')
        url = reverse('meeting_create', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)




