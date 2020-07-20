from django.test import TestCase
from django.urls import reverse, resolve

from ..views import boards_index
from ..models import Board


class BoardsIndexTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Test', description='Test board')
        url = reverse('boards_index')
        self.response = self.client.get(url)

    def test_boards_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_boards_index_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func, boards_index)

    def test_boards_index_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))