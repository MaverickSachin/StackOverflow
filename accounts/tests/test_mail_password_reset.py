from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail
from django.contrib.auth.models import User


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='kevin', email='kevin@gmail.com', password='password1234')
        self.response = self.client.post(reverse('accounts:password_reset'), {'email': 'kevin@gmail.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('kevin', self.email.body)
        self.assertIn('kevin@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEquals(['kevin@gmail.com', ], self.email.to)
