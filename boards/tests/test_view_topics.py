from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from .. import views


class TopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        url = reverse('boards:topics', kwargs={'pk': self.board.pk})
        self.response = self.client.get(url)

    def test_topics_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_topics_view_not_found(self):
        url = reverse('boards:topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_topics_view_url_resolves(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, views.topics)

    def test_topics_view_contains_navigation_links(self):
        home_page_url = reverse('boards:home')
        new_topic_url = reverse('boards:new_topic', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{home_page_url}"')
        self.assertContains(self.response, f'href="{new_topic_url}"')
