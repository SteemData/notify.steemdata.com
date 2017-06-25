import datetime
import sys
from unittest.mock import patch

from tests.base import BaseTests
from src.blockchain_parser import (
    db, handle_transfer, send_mail, send_telegram,
)


class HandleTransferTests(BaseTests):

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_user_set_transfer_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', transfer=True)

        op = {
            "_id" : "b8cec94b7d16dfe22551f785f79b52ac173126f6",
            "from" : "user1",
            "to" : "user2",
            "amount" : "4.726 STEEM",
            "memo" : "",
            "type" : "transfer",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095969,
            "trx_id" : "9dfe1d3f31a12907e73fc74efdd1ad11a18a8581"
        }
        handle_transfer(op)

        mock_mail.assert_called_once_with(
            'user1@example.com',
            'New Steem Event',
            'Received event: transfer\n'
            'Event detail: user1 -> user2 (4.726 STEEM)',
        )
        mock_telegram.assert_called_once_with(
            '@samplechannel',
            'Received event: transfer\n'
            'Event detail: user1 -> user2 (4.726 STEEM)',
        )

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_user_not_set_transfer_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', transfer=False)

        op = {
            "_id" : "b8cec94b7d16dfe22551f785f79b52ac173126f6",
            "from" : "user1",
            "to" : "user2",
            "amount" : "4.726 STEEM",
            "memo" : "",
            "type" : "transfer",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095969,
            "trx_id" : "9dfe1d3f31a12907e73fc74efdd1ad11a18a8581"
        }
        handle_transfer(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)


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
