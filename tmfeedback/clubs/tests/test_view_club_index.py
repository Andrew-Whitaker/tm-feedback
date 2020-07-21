from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ClubIndexView
from ..models import Club


class ClubIndexTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='john', password='12345678')
        self.board = Club.objects.create(name='Test', description='Test board', organizer=user)
        url = reverse('club_index')
        self.response = self.client.get(url)

    def test_club_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_club_index_url_resolves_index_view(self):
        view = resolve('/clubs/')
        self.assertEquals(view.func.view_class, ClubIndexView)

    # def test_boards_index_view_contains_link_to_topics_page(self):
    #     board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
    #     self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
