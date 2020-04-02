from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('settings:password_change')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='kevin', email='kevin@gmail.com', password='old_password')
        self.url = reverse('settings:password_change')
        self.client.login(username='kevin', password='old_password')
        self.response = self.client.post(self.url, data=data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

    def test_redirection(self):
        # a valid form submission should redirect the user
        self.assertRedirects(self.response, reverse('settings:password_change_done'))

    def test_password_changed(self):
        # refresh the user interface from database to get the new password hash updated by the change password view
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        # create a new request to an arbitrary page
        # the resulting response should now have an 'user' to its context, after a successful sign up
        url = reverse('boards:home')
        response = self.client.get(url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        # an invalid form submission should return to the same page
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_did_not_change_password(self):
        # refresh the user instance from the database to make sure we have the latest data
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
