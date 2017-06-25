import datetime
import sys
from unittest.mock import patch

from tests.base import BaseTests
from src.blockchain_parser import (
    parse_blockchain, send_mail, send_telegram,
)


class ParseBlockchainTests(BaseTests):

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_transfer_with_notification(self, mock_mail, mock_telegram):
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
        parse_blockchain(op)

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
    def test_transfer_without_notification(self, mock_mail, mock_telegram):
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
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_transferfromsavings_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', transfer_from_savings=True)

        op = {
            "_id" : "07669d7cd87bcba3d5a6727538a63d0aebca24d1",
            "from" : "user1",
            "request_id" : 1498293207,
            "to" : "user2",
            "amount" : "7.283 STEEM",
            "memo" : "",
            "type" : "transfer_from_savings",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096166,
            "trx_id" : "4e3316dedf5d209533929d5759569077440ce7fa"
        }
        parse_blockchain(op)

        mock_mail.assert_called_once_with(
            'user1@example.com',
            'New Steem Event',
            'Received event: transfer_from_savings\n'
            'Event detail: user1 -> user2 (7.283 STEEM)',
        )
        mock_telegram.assert_called_once_with(
            '@samplechannel',
            'Received event: transfer_from_savings\n'
            'Event detail: user1 -> user2 (7.283 STEEM)',
        )

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_TransferFromSavings_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', transfer_from_savings=False)

        op = {
            "_id" : "07669d7cd87bcba3d5a6727538a63d0aebca24d1",
            "from" : "user1",
            "request_id" : 1498293207,
            "to" : "user2",
            "amount" : "7.283 STEEM",
            "memo" : "",
            "type" : "transfer_from_savings",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096166,
            "trx_id" : "4e3316dedf5d209533929d5759569077440ce7fa"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_WithdrawVesting_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', withdraw_vesting=True)

        op = {
            "_id" : "ec20aae3e32a978b3b16467e47a1ae3cf594ee49",
            "account" : "user1",
            "vesting_shares" : "1236574.074057 VESTS",
            "type" : "withdraw_vesting",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096004,
            "trx_id" : "eb8a2b1b0b569b4a3c3f58516f8efec3a2214e88"
        }
        parse_blockchain(op)

        msg = 'Received event: withdraw_vesting\n' \
              'Account: user1\n' \
              'Vesting shares: 1236574.074057 VESTS'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_WithdrawVesting_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', withdraw_vesting=False)

        op = {
            "_id" : "ec20aae3e32a978b3b16467e47a1ae3cf594ee49",
            "account" : "user1",
            "vesting_shares" : "1236574.074057 VESTS",
            "type" : "withdraw_vesting",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096004,
            "trx_id" : "eb8a2b1b0b569b4a3c3f58516f8efec3a2214e88"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillOrder_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_order=True)

        op = {
            "_id" : "2a823327d073ac4418b9b68b561439d4d5c32522",
            "current_owner" : "user1",
            "current_orderid" : 1498292589,
            "current_pays" : "45.841 STEEM",
            "open_owner" : "user2",
            "open_orderid" : 1000,
            "open_pays" : "64.553 SBD",
            "type" : "fill_order",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "3cddc145ddd17aacffa5a5aad4fbbaa490e097b9"
        }
        parse_blockchain(op)

        msg = 'Received event: fill_order\n' \
              'Current owner: user1\n' \
              'Current pays: 45.841 STEEM\n' \
              'Open owner: user2\n' \
              'Open pays: 64.553 SBD'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillOrder_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_order=False)

        op = {
            "_id" : "2a823327d073ac4418b9b68b561439d4d5c32522",
            "current_owner" : "user1",
            "current_orderid" : 1498292589,
            "current_pays" : "45.841 STEEM",
            "open_owner" : "user2",
            "open_orderid" : 1000,
            "open_pays" : "64.553 SBD",
            "type" : "fill_order",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "3cddc145ddd17aacffa5a5aad4fbbaa490e097b9"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillConvertRequest_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_convert_request=True)

        op = {
            "_id" : "e8506d6d02b30a795a0c94454561c13ad4a9b973",
            "owner" : "user1",
            "requestid" : 1497990374,
            "amount_in" : "27.000 SBD",
            "amount_out" : "12.534 STEEM",
            "type" : "fill_convert_request",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096024,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        msg = 'Received event: fill_convert_request\n' \
              'Owner: user1\n' \
              'Amount in: 27.000 SBD\n' \
              'Amount out: 12.534 STEEM'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillConvertRequest_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_convert_request=False)

        op = {
            "_id" : "e8506d6d02b30a795a0c94454561c13ad4a9b973",
            "owner" : "user1",
            "requestid" : 1497990374,
            "amount_in" : "27.000 SBD",
            "amount_out" : "12.534 STEEM",
            "type" : "fill_convert_request",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096024,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillTransferFromSavings_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_transfer_from_savings=True)

        op = {
            "_id" : "159de2915b1fe2fa68844ea3f6e1d2c1974bef6e",
            "from" : "user1",
            "to" : "user2",
            "amount" : "16.000 STEEM",
            "request_id" : 1498034516,
            "memo" : "",
            "type" : "fill_transfer_from_savings",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096336,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        msg = 'Received event: fill_transfer_from_savings\n' \
              'From: user1\n' \
              'To: user2\n' \
              'Amount: 16.000 STEEM'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillTransferFromSavings_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_transfer_from_savings=False)

        op = {
            "_id" : "159de2915b1fe2fa68844ea3f6e1d2c1974bef6e",
            "from" : "user1",
            "to" : "user2",
            "amount" : "16.000 STEEM",
            "request_id" : 1498034516,
            "memo" : "",
            "type" : "fill_transfer_from_savings",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13096336,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillVestingWithdraw_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_vesting_withdraw=True)

        op = {
            "_id" : "9ce5731a970acae84b961c08a91e9da0c0ec0742",
            "from_account" : "user1",
            "to_account" : "user2",
            "withdrawn" : "827.908252 VESTS",
            "deposited" : "0.400 STEEM",
            "type" : "fill_vesting_withdraw",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        msg = 'Received event: fill_vesting_withdraw\n' \
              'From account: user1\n' \
              'To account: user2\n' \
              'Withdrawn: 827.908252 VESTS\n' \
              'Deposited: 0.400 STEEM'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.blockchain_parser.send_telegram')
    @patch('src.blockchain_parser.send_mail')
    def test_FillVestingWithdraw_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', fill_vesting_withdraw=False)

        op = {
            "_id" : "9ce5731a970acae84b961c08a91e9da0c0ec0742",
            "from_account" : "user1",
            "to_account" : "user2",
            "withdrawn" : "827.908252 VESTS",
            "deposited" : "0.400 STEEM",
            "type" : "fill_vesting_withdraw",
            "timestamp" : datetime.datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

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
