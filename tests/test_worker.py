import sys
from datetime import datetime, timedelta
from unittest.mock import patch
from tests.base import BaseTests
from src.worker import (
    parse_blockchain, find_user_settings, confirm_user_settings, 
    send_mail, send_telegram
)


class ParseBlockchainTests(BaseTests):

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_AccountUpdate_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', account_update=True)

        op = {
            "_id" : "aa742915485383ed29c6d58ca4b36b68cc56e716",
            "type" : "account_update",
            "timestamp" : datetime.utcnow(),
            "account" : "user1",
            "block_num" : 13277829,
            "json_metadata" : "{\"profile\":{\"name\":\"PaulN\",\"about\":\"Husband Father Entrepreneur Soccer\",\"location\":\"Cape Town, South Africa\",\"website\":\"https://cocopan.co.za\"}}",
            "memo_key" : "STM5HxZ49aAbAN975PSHZHCRJaFqfUSgxFJNKHQMw9vWHafJoeS6Z",
            "trx_id" : "63c6fb2abeca96e3e9465cbfe19ec17e92e3fb19"
        }
        parse_blockchain(op)

        msg = 'Received event: account_update (user1)'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_AccountUpdate_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', account_update=False)

        op = {
            "_id" : "aa742915485383ed29c6d58ca4b36b68cc56e716",
            "type" : "account_update",
            "timestamp" : datetime.utcnow(),
            "account" : "user1",
            "block_num" : 13277829,
            "json_metadata" : "{\"profile\":{\"name\":\"PaulN\",\"about\":\"Husband Father Entrepreneur Soccer\",\"location\":\"Cape Town, South Africa\",\"website\":\"https://cocopan.co.za\"}}",
            "memo_key" : "STM5HxZ49aAbAN975PSHZHCRJaFqfUSgxFJNKHQMw9vWHafJoeS6Z",
            "trx_id" : "63c6fb2abeca96e3e9465cbfe19ec17e92e3fb19"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_transfer_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', transfer=True)

        op = {
            "_id" : "b8cec94b7d16dfe22551f785f79b52ac173126f6",
            "from" : "user1",
            "to" : "user2",
            "amount" : "4.726 STEEM",
            "memo" : "",
            "type" : "transfer",
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_transfer_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', '@samplechannel', transfer=False)

        op = {
            "_id" : "b8cec94b7d16dfe22551f785f79b52ac173126f6",
            "from" : "user1",
            "to" : "user2",
            "amount" : "4.726 STEEM",
            "memo" : "",
            "type" : "transfer",
            "timestamp" : datetime.utcnow(),
            "block_num" : 13095969,
            "trx_id" : "9dfe1d3f31a12907e73fc74efdd1ad11a18a8581"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
            "block_num" : 13096166,
            "trx_id" : "4e3316dedf5d209533929d5759569077440ce7fa"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_WithdrawVesting_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', withdraw_vesting=True)

        op = {
            "_id" : "ec20aae3e32a978b3b16467e47a1ae3cf594ee49",
            "account" : "user1",
            "vesting_shares" : "1236574.074057 VESTS",
            "type" : "withdraw_vesting",
            "timestamp" : datetime.utcnow(),
            "block_num" : 13096004,
            "trx_id" : "eb8a2b1b0b569b4a3c3f58516f8efec3a2214e88"
        }
        parse_blockchain(op)

        msg = 'Received event: withdraw_vesting\n' \
              'Account: user1\n' \
              'Vesting shares: 1236574.074057 VESTS'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_WithdrawVesting_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', withdraw_vesting=False)

        op = {
            "_id" : "ec20aae3e32a978b3b16467e47a1ae3cf594ee49",
            "account" : "user1",
            "vesting_shares" : "1236574.074057 VESTS",
            "type" : "withdraw_vesting",
            "timestamp" : datetime.utcnow(),
            "block_num" : 13096004,
            "trx_id" : "eb8a2b1b0b569b4a3c3f58516f8efec3a2214e88"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "3cddc145ddd17aacffa5a5aad4fbbaa490e097b9"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
            "block_num" : 13096024,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
            "block_num" : 13096336,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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
            "timestamp" : datetime.utcnow(),
            "block_num" : 13095963,
            "trx_id" : "0000000000000000000000000000000000000000"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_SetWithdrawVestingRoute_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', set_withdraw_vesting_route=True)

        op = {
            "_id" : "4321826d05b371f518cd44196318d73964f8e588",
            "auto_vest" : False,
            "to_account" : "user2",
            "trx_id" : "13441f93a1bb7f41ebfc95f1d280e44fdacc76f6",
            "timestamp" : datetime.utcnow(),
            "from_account" : "user1",
            "block_num" : 13170400,
            "type" : "set_withdraw_vesting_route",
            "percent" : 10000
        }
        parse_blockchain(op)

        msg = 'Received event: set_withdraw_vesting_route\n' \
              'From account: user1\n' \
              'To account: user2\n' \
              'Percent: 10000'
        mock_mail.assert_called_once_with('user1@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_SetWithdrawVestingRoute_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', set_withdraw_vesting_route=False)

        op = {
            "_id" : "4321826d05b371f518cd44196318d73964f8e588",
            "auto_vest" : False,
            "to_account" : "user2",
            "trx_id" : "13441f93a1bb7f41ebfc95f1d280e44fdacc76f6",
            "timestamp" : datetime.utcnow(),
            "from_account" : "user1",
            "block_num" : 13170400,
            "type" : "set_withdraw_vesting_route",
            "percent" : 10000
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_ChangeRecoveryAccount_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('krishtopa', 'krishtopa@example.com', 
                          '@samplechannel', change_recovery_account=True)

        op = {
            "_id" : "318bb3f2064620b9cea03ffdd635b31b37569596",
            "block_num" : 12879142,
            "trx_id" : "7c44a7e1cb9e09643db901ec474ba8a74971f4de",
            "type" : "change_recovery_account",
            "timestamp" : datetime.utcnow(),
            "new_recovery_account" : "kental",
            "account_to_recover" : "krishtopa",
            "extensions" : [ ]
        }
        parse_blockchain(op)

        msg = 'Received event: change_recovery_account\n' \
              'Account to recover: krishtopa\n' \
              'New recovery account: kental'
        mock_mail.assert_called_once_with('krishtopa@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_ChangeRecoveryAccount_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('user1', 'user1@example.com', 
                          '@samplechannel', change_recovery_account=False)

        op = {
            "_id" : "318bb3f2064620b9cea03ffdd635b31b37569596",
            "block_num" : 12879142,
            "trx_id" : "7c44a7e1cb9e09643db901ec474ba8a74971f4de",
            "type" : "change_recovery_account",
            "timestamp" : datetime.utcnow(),
            "new_recovery_account" : "kental",
            "account_to_recover" : "krishtopa",
            "extensions" : [ ]
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_RequestAccountRecovery_with_notification(self, mock_mail, mock_telegram):
        self.add_settings('mreichardt', 'mreichardt@example.com', 
                          '@samplechannel', request_account_recovery=True)

        op = {
            "_id" : "218aa78e303c4a5e9389a465633639d74609ec0b",
            "trx_id" : "da0e78c22dde8014148092d1bc02e42ab106c81b",
            "account_to_recover" : "mreichardt",
            "type" : "request_account_recovery",
            "block_num" : 13134522,
            "new_owner_authority" : {
                "key_auths" : [
                    [
                        "STM5vX56cxZnj4UoLGSGrzJmoGvsHL3gPtFvGVnAJ8H9dUHNMjQCz",
                        1
                    ]
                ],
                "account_auths" : [ ],
                "weight_threshold" : 1
            },
            "extensions" : [ ],
            "recovery_account" : "steem",
            "timestamp" : datetime.utcnow()
        }
        parse_blockchain(op)

        msg = 'Received event: request_account_recovery\n' \
              'Account to recover: mreichardt\n' + \
              'Recovery account: steem'
        mock_mail.assert_called_once_with('mreichardt@example.com', 'New Steem Event', msg)
        mock_telegram.assert_called_once_with('@samplechannel', msg)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
    def test_RequestAccountRecovery_without_notification(self, mock_mail, mock_telegram):
        self.add_settings('mreichardt', 'mreichardt@example.com', 
                          '@samplechannel', request_account_recovery=False)

        op = {
            "_id" : "218aa78e303c4a5e9389a465633639d74609ec0b",
            "trx_id" : "da0e78c22dde8014148092d1bc02e42ab106c81b",
            "account_to_recover" : "mreichardt",
            "type" : "request_account_recovery",
            "block_num" : 13134522,
            "new_owner_authority" : {
                "key_auths" : [
                    [
                        "STM5vX56cxZnj4UoLGSGrzJmoGvsHL3gPtFvGVnAJ8H9dUHNMjQCz",
                        1
                    ]
                ],
                "account_auths" : [ ],
                "weight_threshold" : 1
            },
            "extensions" : [ ],
            "recovery_account" : "steem",
            "timestamp" : datetime.utcnow()
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 0)
        self.assertEqual(mock_telegram.call_count, 0)

    @patch('src.worker.send_mail')
    def test_send_notification_to_confirmed_settings_only(self, mock_mail):
        self.add_settings('user1', 'a@a.com', account_update=True, confirmed=True, 
                          created_at=datetime.utcnow() - timedelta(days=3))
        self.add_settings('user1', 'b@b.com', account_update=True, confirmed=True, 
                          created_at=datetime.utcnow() - timedelta(days=2))
        self.add_settings('user1', 'c@c.com', account_update=True, confirmed=False, 
                          created_at=datetime.utcnow() - timedelta(days=1))

        op = {
            "_id" : "aa742915485383ed29c6d58ca4b36b68cc56e716",
            "type" : "account_update",
            "timestamp" : datetime.utcnow(),
            "account" : "user1",
            "block_num" : 13277829,
            "json_metadata" : "{\"profile\":{\"name\":\"PaulN\"}}",
            "memo_key" : "STM5HxZ49aAbAN975PSHZHCRJaFqfUSgxFJNKHQMw9vWHafJoeS6Z",
            "trx_id" : "63c6fb2abeca96e3e9465cbfe19ec17e92e3fb19"
        }
        parse_blockchain(op)

        self.assertEqual(mock_mail.call_count, 1)
        mock_mail.assert_called_once_with(
            'b@b.com', 
            'New Steem Event', 
            'Received event: account_update (user1)',
        )


class ConfirmUserSettingsTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.id1 = self.add_settings('user1', 'a@a.com', '@aaa', confirmed=False)
        self.id2 = self.add_settings('user1', 'b@b.com', '@bbb', confirmed=False)
        self.id3 = self.add_settings('user1', 'c@c.com', '@ccc', confirmed=False)

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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

    @patch('src.worker.send_telegram')
    @patch('src.worker.send_mail')
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