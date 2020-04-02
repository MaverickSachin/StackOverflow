from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='kevin', email='kevin@gmail.com', password='password1234')
        # create a valid password reset token based on how a django creates the token internally
        # https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        self.token = default_token_generator.make_token(user=user)

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_password_reset_confirm_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_confirm_resolves_url_view(self):
        view = resolve(f'/accounts/reset/confirm/{self.uid}/{self.token}/')
        self.assertEquals(view.func.view_class, PasswordResetConfirmView)

    def test_password_reset_confirm_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_confirm_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_password_reset_confirm_form_inputs(self):
        # the view must contain two input fields: csrf and two password fields
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='kevin', email='kevin@gmail.com', password='password1234')
        # create a valid password reset token based on how a django creates the token internally
        # https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        self.token = default_token_generator.make_token(user=user)

        # invalidate the token by changing the password
        user.set_password('abcdef1234')
        user.save()

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_password_reset_confirm_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_confirm_html(self):
        url = reverse('accounts:password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, f'href="{url}"')
