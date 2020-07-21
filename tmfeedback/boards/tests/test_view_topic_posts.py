from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import topic_posts
from ..models import Board, Topic, Post


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Test', description='Board for testing.')
        user = get_user_model().objects.create(username='John', email='john@doe.com', password='12345678')
        topic = Topic.objects.create(subject='Test Topic', board=board, started_by=user)
        Post.objects.create(message='Testing 123 Testing 123', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'board_pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func, topic_posts)
