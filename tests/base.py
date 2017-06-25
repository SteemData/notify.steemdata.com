from flask_testing import TestCase
import os
import sys
from unittest.mock import patch

os.environ['MONGO_URI'] = 'mongodb://localhost:27017/steem_notifier_test'
os.environ['MAILGUN_DOMAIN_NAME'] = 'example.com'
os.environ['MAILGUN_API_KEY'] = 'sample_key'
os.environ['TELEGRAM_TOKEN'] = 'sample_token'

from src.blockchain_parser import db
from src.app import app


class BaseTests(TestCase):
    def setUp(self):
        super().setUp()
        self.mailgun_domain_name = os.getenv('MAILGUN_DOMAIN_NAME')
        self.mailgun_api_key = os.getenv('MAILGUN_API_KEY')
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.db = db

    def create_app(self):
        self.app = app
        return self.app

    def tearDown(self):
        super().tearDown()
        db.settings.delete_many({})
        db.blockchains.delete_many({})
        db.processed_blockchains.delete_many({})

    def add_settings(self, username, email=None, telegram_channel_id=None,
                     account_update=False, change_recovery_account=False,
                     request_account_recovery=False, transfer=False,
                     transfer_from_savings=False, set_withdraw_vesting_route=False,
                     withdraw_vesting=False, fill_order=False,
                     fill_convert_request=False, fill_transfer_from_savings=False,
                     fill_vesting_withdraw=False):
        db.settings.insert_one({
            'username': username,
            'email': email,
            'telegram_channel_id': telegram_channel_id,
            'account_update': account_update,
            'change_recovery_account': change_recovery_account,
            'request_account_recovery': request_account_recovery,
            'transfer': transfer,
            'transfer_from_savings': transfer_from_savings,
            'set_withdraw_vesting_route': set_withdraw_vesting_route,
            'withdraw_vesting': withdraw_vesting,
            'fill_order': fill_order,
            'fill_convert_request': fill_convert_request,
            'fill_transfer_from_savings': fill_transfer_from_savings,
            'fill_vesting_withdraw': fill_vesting_withdraw,
        })
