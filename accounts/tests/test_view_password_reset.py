from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)

    def test_password_reset_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_url_resolves_view(self):
        view = resolve('/accounts/reset/')
        self.assertEquals(view.func.view_class, PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_password_reset_form_inputs(self):
        # the view must contains two inputs: csrf, email
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='kevin', email='kevin@gmail.com', password='password1234')
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': 'kevin@gmail.com'})

    def test_password_reset_redirect(self):
        # a valid form submission should redirect the user to 'password_reset_done'
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, data={'email': 'donotexist@gmail.com'})

    def test_redirection(self):
        # even invalid emails in the database should redirect the user to 'password_reset_done' view
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
