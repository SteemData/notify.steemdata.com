from ..base import BaseTests
from werkzeug.datastructures import MultiDict
from blueprints.users.forms import RegisterForm, LoginForm


class RegisterFormTests(BaseTests):
    def test_valid_data(self):
        form = RegisterForm(MultiDict([
            ('username', 'nash'),
            ('email', 'nash@example.com'),
            ('password', 's3cr3t'),
            ('confirm_password', 's3cr3t'),
        ]))

        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = RegisterForm(MultiDict([
            ('username', ''),
            ('email', 'xxx'),
            ('password', ''),
            ('confirm_password', ''),
        ]))

        self.assertFalse(form.validate())
        self.assertEqual(len(form.errors), 4)
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'Invalid email address.')
        self.assertEqual(form.errors['password'][0], 'This field is required.')
        self.assertEqual(form.errors['confirm_password'][0], 'This field is required.')

    def test_unique_username(self):
        form = RegisterForm(MultiDict([
            ('username', 'bob'),
            ('email', 'bob@gmail.com'),
            ('password', '12345'),
            ('confirm_password', '12345'),
        ]))

        self.assertFalse(form.validate())
        self.assertEqual(form.errors['username'][0], 'This username is already taken.')


class LoginFormTests(BaseTests):
    def test_valid_data(self):
        form = LoginForm(MultiDict([
            ('username', 'user'),
            ('password', 's3cr3t'),
        ]))

        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = LoginForm(MultiDict([
            ('username', ''),
            ('password', ''),
        ]))

        self.assertFalse(form.validate())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        self.assertEqual(form.errors['password'][0], 'This field is required.')
