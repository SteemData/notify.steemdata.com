from ..base import BaseTests


class RegisterTests(BaseTests):
    def test_render_the_template(self):
        response = self.client.get('/users/register')
        
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/register.html')

    def test_valid_data(self):
        count = self.mongo.db.users.count()

        response = self.client.post('/users/register', data={
            'username': 'nash',
            'email': 'nash@gmail.com',
            'password': 's3cr3t',
            'confirm_password': 's3cr3t',
        })

        new_count = self.mongo.db.users.count()
        self.assertEqual(new_count, count+1)

    def test_invalid_data(self):
        count = self.mongo.db.users.count()

        response = self.client.post('/users/register', data={
            'username': '',
            'email': 'xxx',
            'password': 'yyy',
            'confirm_password': '',
        })

        new_count = self.mongo.db.users.count()
        form = self.get_context_variable('form')
        self.assertEqual(new_count, count)
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'Invalid email address.')
        self.assertEqual(form.errors['password'][0], 'Both password must match.')
        self.assertEqual(form.errors['confirm_password'][0], 'This field is required.')


class LoginTests(BaseTests):
    def test_render_the_template(self):
        response = self.client.get('/users/login')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')

    def test_valid_login(self):
        response = self.client.post('/users/login', data={
            'username': 'bob',
            'password': 's3cr3t',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_invalid_login(self):
        response = self.client.post('/users/login', data={
            'username': 'xxx',
            'password': 'yyy',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Invalid username/password' in response.data)
