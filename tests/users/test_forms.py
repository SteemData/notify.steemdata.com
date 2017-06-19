import unittest
from werkzeug.datastructures import MultiDict
from blueprints.users.forms import LoginForm


class LoginFormTests(unittest.TestCase):
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
