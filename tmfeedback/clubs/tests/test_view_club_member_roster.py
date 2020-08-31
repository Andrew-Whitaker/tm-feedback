from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubMemberRoster
from ..models import Club


class ClubMemberRosterTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.club.members.add(self.user)
        self.client.login(username='john', password='12345678')
        self.url = reverse('clubs:member_roster', kwargs={'club_id': self.club.id})
        self.response = self.client.get(self.url)

    def test_club_roster_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_roster_view_not_found_status_code(self):
        bad_url = reverse('clubs:member_roster', kwargs={'club_id': 13})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_club_roster_url_resolves_club_roster_view(self):
        view = resolve('/clubs/{0}/roster/'.format(self.club.id))
        self.assertEquals(view.func.view_class, ClubMemberRoster)

    def test_club_roster_view_contains_nav_links(self):
        home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        index_url = reverse('clubs:index', kwargs={})
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(index_url))

    # def test_club_roster_csrf(self):
    #     self.assertContains(self.response, 'csrfmiddlewaretoken')


class LoginRequiredRosterTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        self.user = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.club.members.add(self.user)
        self.url = reverse('clubs:member_roster', kwargs={'club_id': self.club.id})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
