from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from ..views import reply_topic
from ..forms import PostForm


class ReplyTopicTestCase(TestCase):
    # base test case to be used in all 'reply_topic' view tests
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is Django discussion board.')
        self.username = 'kevin'
        self.password = 'password1234'
        self.user = User.objects.create_user(username=self.username, email='kevin@gmail.com', password=self.password)
        self.topic = Topic.objects.create(subject='hello world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='hello world!!', topic=self.topic, created_by=self.user)
        self.url = reverse('boards:reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('accounts:login')
        self.response = self.client.get(self.url)
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_view_reply_topic_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_resolves_url(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        # the view must contain two inputs: csrf, message text area
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={'message': 'hello world'})

    def test_redirection(self):
        # a valid form should redirect the user
        posts_url = reverse('boards:posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        post_number = self.post.pk + 1
        topic_posts_url = f'{posts_url}?page=1#{post_number}'
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        # the total post count should be 2: the one created in the 'ReplyTopicTestCase' setUp
        # and another created by the post data in this class
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        # submit an empty dictionary to the 'reply_topic' form
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={})

    def test_view_status_code(self):
        # an invalid form submission should return to the same page
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
