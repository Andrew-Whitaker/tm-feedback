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
        url = reverse('meeting_list', kwargs={'club_id': self.club.id})
        self.response = self.client.get(url)

    def test_meeting_list_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_meeting_list_view_not_found_status_code(self):
        bad_url = reverse('meeting_list', kwargs={'club_id': 13})
        response = self.client.get(bad_url)
        self.assertEquals(response.status_code, 404)

    def test_meeting_list_url_resolves_index_view(self):
        view = resolve('/clubs/1/meetings/')
        self.assertEquals(view.func.view_class, MeetingListView)

    def test_meeting_list_view_contains_breadcrumb_links(self):
        # User should have breadcrumb link back to their club home page
        club_home_url = reverse('club_home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

