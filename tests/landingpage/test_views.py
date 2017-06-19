from ..base import BaseTests


class HomepageTests(BaseTests):
    def test_anonymous_user(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login')

    def test_valid_user(self):
        self.login('bob', 's3cr3t')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('landingpage/home.html')
