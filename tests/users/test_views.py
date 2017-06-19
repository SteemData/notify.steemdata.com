from flask_testing import TestCase
from app import create_app


class LoginTests(TestCase):
    def create_app(self):
        return create_app()

    def test_render_the_template(self):
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')
