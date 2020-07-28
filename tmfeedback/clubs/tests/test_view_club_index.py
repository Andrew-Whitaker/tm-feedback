from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubIndexView
from ..models import Club


class ClubIndexTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='john', password='12345678')
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=user)
        url = reverse('club_index')
        self.response = self.client.get(url)

    def test_club_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_index_url_resolves_index_view(self):
        view = resolve('/clubs/')
        self.assertEquals(view.func.view_class, ClubIndexView)

    def test_club_index_view_contains_nav_links(self):
        club_url = reverse('club_home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_url))
