import sys
from datetime import datetime, timedelta
from unittest.mock import patch
from tests.base import BaseTests
from src.methods import find_user_settings, send_mail, send_telegram


class FindUserSettingsTests(BaseTests):
    today = datetime.utcnow()
    yesterday = datetime.utcnow() - timedelta(days=1)
    twodaysago = datetime.utcnow() - timedelta(days=2)

    def test_get_the_latest_confirmed_settings(self):
        id_1 = self.add_settings('a', 'a@a.com', confirmed=True, created_at=self.twodaysago)
        id_2 = self.add_settings('a', 'b@b.com', confirmed=True, created_at=self.yesterday)
        id_3 = self.add_settings('a', 'c@c.com', confirmed=False, created_at=self.today)

        settings = find_user_settings('a')

        self.assertEqual(settings.get('_id'), id_2)
        self.assertEqual(settings.get('email'), 'b@b.com')

    def test_no_confirmed_settings(self):
        self.add_settings('a', 'a@a.com', confirmed=False, created_at=self.twodaysago)
        self.add_settings('a', 'b@b.com', confirmed=False, created_at=self.yesterday)
        self.add_settings('a', 'c@c.com', confirmed=False, created_at=self.today)

        self.assertEqual(find_user_settings('a'), dict())


class SendMailTests(BaseTests):

    @patch('requests.post')
    def test_success_email(self, mock_r):
        send_mail('bob@example.com', 'sample email', 'sample message')

        mock_r.assert_called_with(
            'https://api.mailgun.net/v3/%s/messages' % self.mailgun_domain_name,
            auth={'api': self.mailgun_api_key},
            data={
                'from': 'noreply@%s' % self.mailgun_domain_name, 
                'to': ['bob@example.com'], 
                'subject': 'sample email', 
                'text': 'sample message',
            },
        )
        if hasattr(sys.stdout, 'getvalue'):
            self.assertEqual(
                sys.stdout.getvalue(), 
                'Sent mail to: bob@example.com.\n',
            )

    @patch('requests.post')
    def test_failed_email(self, mock_r):
        mock_r.side_effect = Exception('Something went wrong.')

        send_mail('user@example.com', 'xxx', 'yyy')

        if hasattr(sys.stdout, 'getvalue'):
            self.assertEqual(
                sys.stdout.getvalue(), 
                'Failed sending email to: user@example.com.\n',
            )


class SendTelegramTests(BaseTests):

    @patch('requests.post')
    def test_success(self, mock_r):
        send_telegram('@samplechannel', 'sample message')

        mock_r.assert_called_with(
            'https://api.telegram.org/bot%s/sendMessage' % self.telegram_token,
            data={
                'chat_id': '@samplechannel',
                'text': 'sample message',
            }
        )
        if hasattr(sys.stdout, 'getvalue'):
            self.assertEqual(
                sys.stdout.getvalue(), 
                'Sent notification to: @samplechannel.\n',
            )

    @patch('requests.post')
    def test_failed(self, mock_r):
        mock_r.side_effect = Exception('something went wrong')

        send_telegram('@xxx', 'yyy')

        if hasattr(sys.stdout, 'getvalue'):
            self.assertEqual(
                sys.stdout.getvalue(), 
                'Failed sending telegram message to: @xxx.\n',
            )
