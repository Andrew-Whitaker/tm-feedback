from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubManageRequestsView
from ..models import Club


class ClubManageRequestTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing', organizer=self.user)
        self.club.members.add(self.user)
        self.client.login(username='john', password='12345678')
        self.url = reverse('clubs:membership_requests', kwargs={'club_id': self.club.id})
        self.response = self.client.get(self.url)

    def test_club_requests_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_requests_view_not_found_status_code(self):
        bad_url = reverse('clubs:membership_requests', kwargs={'club_id': 13})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_club_requests_url_resolves_membership_requests_view(self):
        view = resolve('/clubs/{0}/membership_requests/'.format(self.club.id))
        self.assertEquals(view.func.view_class, ClubManageRequestsView)

    def test_club_requests_view_contains_breadcrumb_links(self):
        home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(home_url))



    # def test_club_roster_csrf(self):
    #     self.assertContains(self.response, 'csrfmiddlewaretoken')


class PermissionsRequiredRequestsTests(TestCase):
    def setUp(self):
        self.organizer = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.user = get_user_model().objects.create_user(username='jane', email='jane@doe.com', password='12345678')
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing', organizer=self.organizer)
        self.url = reverse('clubs:membership_requests', kwargs={'club_id': self.club.id})

    def test_login_redirection(self):
        self.response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

    def test_organizer_success(self):
        self.client.login(username='john', password='12345678')
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_non_organizer_forbidden(self):
        self.client.login(username='jane', password='12345678')
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 403)


class DisplayingRequestsTest(TestCase):

    def test_requests_list_contains_member_nav_links(self):
        # There should be at least one member in the roster list with a link
        # to their user profile page
        self.assertTrue(False, 'Have not created links to user profiles from club membership requests page.')
        # TODO: Make a real test once user profiles have been implemented


class TestFunctionality(TestCase):
    def test_filler_not_completed(self):
        self.assertTrue(False, 'Have not created real tests for the functionality of this page.')

