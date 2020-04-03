from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetDoneView


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_done')
        self.response = self.client.get(url)

    def test_password_reset_done_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_done_url_resolves_view(self):
        view = resolve('/accounts/reset/done/')
        self.assertEquals(view.func.view_class, PasswordResetDoneView)
