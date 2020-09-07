from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubHomeView
from ..models import Club
from meetings.models import Meeting


class ClubHomeTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        self.meeting = Meeting.objects.create(date='2020-08-28', theme='Integrity', club=self.club)
        get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        self.client.login(username='john', password='12345678')
        self.url = reverse('clubs:home', kwargs={'club_id': 1})
        self.response = self.client.get(self.url)

    def test_club_home_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_home_view_not_found_status_code(self):
        bad_url = reverse('clubs:home', kwargs={'club_id': 13})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_club_home_url_resolves_club_home_view(self):
        view = resolve('/clubs/1/')
        self.assertEquals(view.func.view_class, ClubHomeView)

    def test_club_home_view_contains_breadcrumb_links(self):
        club_index_url = reverse('clubs:index')
        self.assertContains(self.response, 'href="{0}"'.format(club_index_url))

    def test_club_home_view_contains_meeting_nav_links(self):
        # There should be a link to access the full list of meetings the club has had
        meeting_index_url = reverse('clubs:meeting_index', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_index_url))

        # There should be a link that redirects to the meeting create page for a club
        meeting_creation_url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_creation_url))

        # There should be at least one meeting in the short meeting list with a link
        # to that meeting detail page
        meeting_detail_url = reverse('meetings:detail', kwargs={'meeting_pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_detail_url))

    def test_club_home_view_contains_member_nav_links(self):
        # There should be a link to access the full member roster
        roster_url = reverse('clubs:member_roster', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(roster_url))

        # There should be at least one member in the short roster list with a link
        # to their user profile page
        self.assertTrue(False, 'Have not created links to user profiles from club home page.')
        # TODO: Make a real test once user profiles have been implemented


class ClubHomeMembershipButtonTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', id=1, description='Club for testing')
        john = get_user_model().objects.create_user(username='john', email='john@doe.com', password='12345678')
        jane = get_user_model().objects.create_user(username='jane', email='jane@doe.com', password='12345678')
        james = get_user_model().objects.create_user(username='james', email='james@doe.com', password='12345678')
        self.club.members.add(john)
        self.club.membership_requests.add(jane)

    def test_login_required(self):
        url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-primary" disabled>Login to Join</button>')

    def test_non_member_not_requested(self):
        self.client.login(username='james', password='12345678')
        url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Request Membership</button>')

    def test_non_member_has_requested(self):
        self.client.login(username='jane', password='12345678')
        url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-info" disabled>Pending Approval</button>')

    def test_member(self):
        self.client.login(username='john', password='12345678')
        url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        response = self.client.get(url)
        self.assertContains(response, '<button type="button" class="btn btn-success" disabled>Member</button>')
