from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetCompleteView


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_complete')
        self.response = self.client.get(url)

    def test_password_reset_complete_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_complete_resolves_view(self):
        view = resolve('/accounts/reset/complete/')
        self.assertEquals(view.func.view_class, PasswordResetCompleteView)
