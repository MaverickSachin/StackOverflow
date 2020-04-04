from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Post, Topic
from ..views import PostUpdateView
from django.forms import ModelForm


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        self.username = 'kevin'
        self.password = 'password1234'
        self.user = User.objects.create_user(username=self.username, email='kevin@gmail.com', password=self.password)
        self.topic = Topic.objects.create(subject='hello world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='hello world!!', topic=self.topic, created_by=self.user)
        self.url = reverse('boards:edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.username = 'peter'
        self.password = 'password1234'
        self.user = User.objects.create_user(username=self.username, email='peter@gmail.com', password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_view_status_code(self):
        # a topic should be edited only by its owner
        # Unauthorized users should get a 404 response (Page not found)
        self.assertEquals(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_resolves_url(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/posts/{self.post.pk}/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_view_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_view_form_inputs(self):
        # the view must contains two inputs: csrf and message text area
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={'message': 'edited message'})

    def test_redirection(self):
        # a valid form submission should redirect the user
        posts_url = reverse('boards:posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, posts_url)

    def test_view_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'edited message')


class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={})

    def test_view_status_code(self):
        # an invalid form submission should return to the same page
        self.assertEquals(self.response.status_code, 200)

    def test_view_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
