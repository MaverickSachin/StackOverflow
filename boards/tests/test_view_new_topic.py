from django.test import TestCase
from django.urls import reverse
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
from ..forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        self.user = User.objects.create_user(username='admin', email='admin@gmail.com', password='password_123')
        self.client.login(username='admin', password='password_123')
        self.url = reverse('boards:new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(self.url)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_view_not_found(self):
        url = reverse('boards:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_contains_navigation_links(self):
        home_url = reverse('boards:home')
        topics_url = reverse('boards:topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{topics_url}"')
        self.assertContains(self.response, f'href="{home_url}"')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_valid_post_data(self):
        data = {
            'subject': 'Test title',
            'message': 'This is testing message'
        }
        self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        # Invalid post data should not redirect
        # The expected behavior is to show the form again with validation errors
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        # Invalid post data should not redirect
        # The expected behavior is to show the form again with validation errors
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        self.url = reverse('boards:new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('accounts:login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
