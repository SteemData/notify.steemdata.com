from ..base import BaseTests


class HomepageTests(BaseTests):
    def test_redirect_to_login_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login')
