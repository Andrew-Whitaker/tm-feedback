from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubHomeView
from ..models import Club


class ClubHomeTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.client.login(username='john', password='12345678')

    def test_club_home_view_success_status_code(self):
        url = reverse('club_home', kwargs={'club_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_club_home_view_not_found_status_code(self):
        url = reverse('club_home', kwargs={'club_id': 13})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_club_home_url_resolves_club_home_view(self):
        view = resolve('/clubs/1/')
        self.assertEquals(view.func.view_class, ClubHomeView)

    def test_club_home_view_contains_nav_links(self):
        url = reverse('club_home', kwargs={'club_id': self.club.id})
        roster_url = reverse('club_member_roster', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(roster_url))


class ClubHomeMembershipButtonTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        john = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        jane = get_user_model().objects.create_user(username='jane', email='jane@doe.com', password='12345678')
        james = get_user_model().objects.create_user(username='james', email='james@doe.com', password='12345678')
        self.club.members.add(john)
        self.club.membership_requests.add(jane)

    def test_login_required(self):
        url = reverse('club_home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-primary" disabled>Login to Join</button>')

    def test_non_member_not_requested(self):
        self.client.login(username='james', password='12345678')
        url = reverse('club_home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Request Membership</button>')

    def test_non_member_has_requested(self):
        self.client.login(username='jane', password='12345678')
        url = reverse('club_home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-info" disabled>Pending Approval</button>')

    def test_member(self):
        self.client.login(username='john', password='12345678')
        url = reverse('club_home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-success" disabled>Member</button>')
