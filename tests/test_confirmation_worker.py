from datetime import datetime, timedelta
from unittest.mock import patch
from tests.base import BaseTests
from src.confirmation_worker import confirm_user_settings


class ConfirmUserSettingsTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.id1 = self.add_settings('user1', 'a@a.com', '@aaa', confirmed=False)
        self.id2 = self.add_settings('user1', 'b@b.com', '@bbb', confirmed=False)
        self.id3 = self.add_settings('user1', 'c@c.com', '@ccc', confirmed=False)

    @patch('src.confirmation_worker.send_telegram')
    @patch('src.confirmation_worker.send_mail')
    def test_valid_data(self, mock_mail, mock_telegram):
        op = {
            "_id" : "1f6e047c59bea977a2c513716954538e0b04a8e9",
            "from" : "user1",
            "memo" : self.id2,
            "timestamp" : datetime.utcnow(),
            "type" : "transfer",
            "trx_id" : "e5a9f188ffc16f8cda143a28f13520a46595a432",
            "block_num" : 55655,
            "amount" : {
                "asset" : "STEEM",
                "amount" : 0.001
            },
            "to" : self.steem_wallet, 
        }
        confirm_user_settings(op)

        item1 = self.db.settings.find_one({'_id': self.id1})
        item2 = self.db.settings.find_one({'_id': self.id2})
        item3 = self.db.settings.find_one({'_id': self.id3})
        self.assertEqual(item1['confirmed'], False)
        self.assertEqual(item2['confirmed'], True)
        self.assertEqual(item3['confirmed'], False)

        message = 'You have made the following changes:\n' + \
                  'Email: b@b.com\n' + \
                  'Telegram: @bbb\n' + \
                  'Notify account_update: False\n' + \
                  'Notify change_recovery_account: False\n' + \
                  'Notify request_account_recovery: False\n' + \
                  'Notify transfer: False\n' + \
                  'Notify transfer_from_savings: False\n' + \
                  'Notify set_withdraw_vesting_route: False\n' + \
                  'Notify withdraw_vesting: False\n' + \
                  'Notify fill_order: False\n' + \
                  'Notify fill_convert_request: False\n' + \
                  'Notify fill_transfer_from_savings: False\n' + \
                  'Notify fill_vesting_withdraw: False\n'
        mock_mail.assert_called_once_with('b@b.com', 'Update confirmed', message)
        mock_telegram.assert_called_once_with('@bbb', message)

    @patch('src.confirmation_worker.send_telegram')
    @patch('src.confirmation_worker.send_mail')
    def test_invalid_amount(self, mock_mail, mock_telegram):
        op = {
            "_id" : "1f6e047c59bea977a2c513716954538e0b04a8e9",
            "from" : "user1",
            "memo" : self.id2,
            "timestamp" : datetime.utcnow(),
            "type" : "transfer",
            "trx_id" : "e5a9f188ffc16f8cda143a28f13520a46595a432",
            "block_num" : 55655,
            "amount" : {
                "asset" : "STEEM",
                "amount" : 0.0000001
            },
            "to" : self.steem_wallet, 
        }
        confirm_user_settings(op)

        item1 = self.db.settings.find_one({'_id': self.id1})
        item2 = self.db.settings.find_one({'_id': self.id2})
        item3 = self.db.settings.find_one({'_id': self.id3})
        self.assertEqual(item1['confirmed'], False)
        self.assertEqual(item2['confirmed'], False)
        self.assertEqual(item3['confirmed'], False)
        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.confirmation_worker.send_telegram')
    @patch('src.confirmation_worker.send_mail')
    def test_invalid_asset(self, mock_mail, mock_telegram):
        op = {
            "_id" : "1f6e047c59bea977a2c513716954538e0b04a8e9",
            "from" : "user1",
            "memo" : self.id2,
            "timestamp" : datetime.utcnow(),
            "type" : "transfer",
            "trx_id" : "e5a9f188ffc16f8cda143a28f13520a46595a432",
            "block_num" : 55655,
            "amount" : {
                "asset" : "BTC",
                "amount" : 0.001
            },
            "to" : self.steem_wallet, 
        }
        confirm_user_settings(op)

        item1 = self.db.settings.find_one({'_id': self.id1})
        item2 = self.db.settings.find_one({'_id': self.id2})
        item3 = self.db.settings.find_one({'_id': self.id3})
        self.assertEqual(item1['confirmed'], False)
        self.assertEqual(item2['confirmed'], False)
        self.assertEqual(item3['confirmed'], False)
        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)
