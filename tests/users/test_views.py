from ..base import BaseTests


class RegisterTests(BaseTests):
    def test_render_the_template(self):
        response = self.client.get('/users/register')
        
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/register.html')


class LoginTests(BaseTests):
    def test_render_the_template(self):
        response = self.client.get('/users/login')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')
