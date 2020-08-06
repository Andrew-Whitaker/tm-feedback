from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import MeetingDetailView
from ..models import Meeting
from clubs.models import Club


class MeetingDetailTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='john', password='12345678')
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=user)
        self.meeting = Meeting.objects.create(date='2020-07-28', theme='Integrity', club=self.club)
        url = reverse('meeting_detail', kwargs={'club_id': self.club.id, 'meeting_pk': self.meeting.pk})
        self.response = self.client.get(url)

    def test_meeting_detail_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_meeting_detail_view_not_found_status_code(self):
        bad_url = reverse('meeting_detail', kwargs={'club_id': 1, 'meeting_pk': 999})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_meeting_detail_url_resolves_index_view(self):
        view = resolve('/clubs/{}/meetings/{}/'.format(self.club.id, self.meeting.pk))
        self.assertEquals(view.func.view_class, MeetingDetailView)

    def test_meeting_detail_view_contains_breadcrumb_links(self):
        # User should have breadcrumb link back to their club home page
        club_home_url = reverse('club_home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # User should have breadcrumb link back to the meeting list of that club
        meeting_list_url = reverse('meeting_list', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(meeting_list_url))

