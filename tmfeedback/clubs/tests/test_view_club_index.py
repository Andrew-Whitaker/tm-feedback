from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubIndexView
from ..models import Club


class ClubIndexTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='john', password='12345678')
        self.club = Club.objects.create(name='Test', id=1, description='Test board', organizer=user)
        url = reverse('clubs:index')
        self.response = self.client.get(url)

    def test_club_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_index_url_resolves_index_view(self):
        view = resolve('/clubs/')
        self.assertEquals(view.func.view_class, ClubIndexView)

    def test_club_index_view_contains_nav_links(self):
        # should exist at least one club in the list with a link to the home page
        club_home_url = reverse('clubs:home', kwargs={'club_id': self.club.id})
        self.assertContains(self.response, 'href="{0}"'.format(club_home_url))

        # should exist a button that redirects to club creation page
        club_creation_url = reverse('clubs:create')
        self.assertContains(self.response, 'href="{0}"'.format(club_creation_url))
