from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import MeetingListView
from ..models import Meeting
from clubs.models import Club


class MeetingListTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='john', password='12345678')
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=user)
        self.meeting = Meeting.objects.create(date='2020-07-28', theme='Integrity', club=self.club)
        url = reverse('clubs:meeting_index', kwargs={'club_id': self.club.id})
        self.response = self.client.get(url)

    def test_meeting_list_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_meeting_list_view_not_found_status_code(self):
        bad_url = reverse('clubs:meeting_index', kwargs={'club_id': 13})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_meeting_list_url_resolves_index_view(self):
        view = resolve('/clubs/{}/meetings/'.format(self.club.id))
        self.assertEquals(view.func.view_class, MeetingListView)

    def test_meeting_list_view_contains_breadcrumb_links(self):
        # User should have breadcrumb link back to their club home page
        club_home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

    def test_meeting_list_view_contains_meeting_nav_links(self):
        # Should be a link to at least one meeting detail page
        meeting_detail_url = reverse('meetings:detail', kwargs={'meeting_pk': self.meeting.pk})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_detail_url))

        # Should be a link to edit that meeting.
        self.assertTrue(False, 'TODO: Make this test - Edit hyperlink should navigate to meeting edit page.')

    def test_meeting_list_view_contains_button_links(self):
        # Should be a button with a link to create meeting page
        meeting_create_url = reverse('clubs:create_meeting', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_create_url))
