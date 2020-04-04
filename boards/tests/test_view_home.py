from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from .. import views


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        url = reverse('boards:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func, views.home)

    def test_home_view_contains_link_to_topics_page(self):
        url = reverse('boards:topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{url}"')
