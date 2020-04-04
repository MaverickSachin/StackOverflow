from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from ..models import Board, Topic, Post
from ..views import PostListView


class PostsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        self.user = User.objects.create_user(username='kevin', email='kevin@gmail.com', password='password1234')
        self.topic = Topic.objects.create(subject='hello world', board=self.board, starter=self.user)
        Post.objects.create(message='hello world!!', topic=self.topic, created_by=self.user)
        url = reverse('boards:posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(url)

    def test_view_posts_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_posts_resolves_url(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/')
        self.assertEquals(view.func.view_class, PostListView)
