from werkzeug.datastructures import MultiDict
from tests.base import BaseTests
from src.app import NotificationSettingsForm


class NotificationSettingsFormTests(BaseTests):
    def test_valid_data(self):
        form = NotificationSettingsForm(MultiDict([
            ('email', 'user@example.com'),
            ('telegram_channel_id', '@samplechannel'),
            ('account_update', False),
            ('change_recovery_account', False),
            ('request_account_recovery', False),
            ('transfer', False),
            ('transfer_from_savings', False),
            ('set_withdraw_vesting_route', False),
            ('withdraw_vesting', False),
            ('fill_order', False),
            ('fill_convert_request', False),
            ('fill_transfer_from_savings', False),
            ('fill_vesting_withdraw', False),
        ]))

        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = NotificationSettingsForm(MultiDict([
            ('email', 'xxx'),
            ('telegram_channel_id', 'yyy'),
        ]))

        self.assertFalse(form.validate())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(
            form.errors['email'][0], 
            'Invalid email address.',
        )
        self.assertEqual(
            form.errors['telegram_channel_id'][0], 
            'Wrong format for telegram channel ID.',
        )


class SettingsTests(BaseTests):
    def test_render_the_template(self):
        response = self.client.get('/user1')

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('settings.html')

    def test_insert_with_valid_data(self):
        numrows = self.db.settings.count()

        response = self.client.post('/user1', data={
            'email': 'user1@example.com',
            'telegram_channel_id': '@samplechannel',
        })

        self.assertEqual(self.db.settings.count(), numrows+1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user1')

    def test_insert_with_invalid_data(self):
        numrows = self.db.settings.count()

        response = self.client.post('/user1', data={
            'email': 'xxx',
            'telegram_channel_id': 'yyy',
        })

        form = self.get_context_variable('form')
        self.assertEqual(self.db.settings.count(), numrows)
        self.assertEqual(len(form.errors), 2)

    def test_update_with_valid_data(self):
        self.add_settings('user1', email='user1@example.com', transfer=False)
        numrows = self.db.settings.count()

        response = self.client.post('/user1', data={
            'email': 'user1@example.com',
            'telegram_channel_id': '@samplechannel',
            'transfer': True,
        })

        self.assertEqual(self.db.settings.count(), numrows)
        settings = self.db.settings.find_one({'username': 'user1'})
        self.assertEqual(settings['email'], 'user1@example.com')
        self.assertEqual(settings['telegram_channel_id'], '@samplechannel')
        self.assertEqual(settings['transfer'], True)
