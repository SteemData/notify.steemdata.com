from datetime import datetime, timedelta
from werkzeug.datastructures import MultiDict
from tests.base import BaseTests
from src.app import NotificationSettingsForm, hash_op


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
    threedaysago = datetime.utcnow() - timedelta(days=3)
    twodaysago = datetime.utcnow() - timedelta(days=2)
    yesterday = datetime.utcnow() - timedelta(days=1)
    today = datetime.utcnow()

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
        self.add_settings(
            'user1', 
            email='user1@example.com', 
            transfer=False, 
            confirmed=True, 
            created_at=datetime.utcnow() - timedelta(days=1),
        )
        numrows = self.db.settings.count()

        response = self.client.post('/user1', data={
            'email': 'user1@example.com',
            'telegram_channel_id': '@samplechannel',
            'transfer': True,
        })

        self.assertEqual(self.db.settings.count(), numrows+1)
        try:
            rows = self.db.settings.find({'username': 'user1'}).sort('created_at', -1)
            settings = rows[0]
        except Exception as e:
            self.fail('Should not raise exception here.')
        self.assertEqual(settings['email'], 'user1@example.com')
        self.assertEqual(settings['telegram_channel_id'], '@samplechannel')
        self.assertEqual(settings['transfer'], True)
        self.assertEqual(settings['confirmed'], False)

    def test_display_last_settings(self):
        self.add_settings('user1', email='a@a.com', confirmed=True, created_at=self.threedaysago)
        self.add_settings('user1', email='b@b.com', confirmed=True, created_at=self.twodaysago)

        response = self.client.get('/user1')

        last_settings = self.get_context_variable('last_settings')
        self.assertEqual(last_settings, dict())

        self.add_settings('user1', email='c@c.com', confirmed=False, created_at=self.yesterday)

        response = self.client.get('/user1')

        last_settings = self.get_context_variable('last_settings')
        self.assertEqual(last_settings.get('email'), 'b@b.com')

        self.add_settings('user1', email='d@d.com', confirmed=False, created_at=self.today)

        response = self.client.get('/user1')

        last_settings = self.get_context_variable('last_settings')
        self.assertEqual(last_settings.get('email'), 'b@b.com')


class HashOpTests(BaseTests):
    op = {
        "_id": "2bf8c1efd5a3e6112bd6fae5ad7fd6e839f77203", 
        "email": "bob@example.com", 
        "telegram_channel_id": "@bob", 
        "created_at": datetime.utcnow(),
    }

    def test_hash_op(self):
        hash1 = hash_op(self.op)
        self.assertEqual(len(hash1), 40)

    def test_hashes_should_be_unique(self):
        hash1 = hash_op(self.op)
        self.op['created_at'] = datetime.utcnow() + timedelta(seconds=1)

        hash2 = hash_op(self.op)

        self.assertNotEqual(hash1, hash2)
