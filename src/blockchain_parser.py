#!/usr/bin/env python
# encoding: utf-8

import os
from contextlib import suppress
from steem.blockchain import Blockchain
import requests
from pymongo import MongoClient


mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/steem_notifier')
client = MongoClient(mongo_uri)
db = client[mongo_uri.split('/')[-1]]


def run():
    b = Blockchain()
    types = [
        'account_update',
        'change_recovery_account',
        'request_account_recovery',
        'transfer',
        'transfer_from_savings',
        'set_withdraw_vesting_route',
        'withdraw_vesting',
        'fill_order',
        'fill_convert_request',
        'fill_transfer_from_savings',
        'fill_vesting_withdraw',
    ]
    for operation in b.stream():
        if operation['type'] in types:
            send_notification(operation)


def send_notification(operation):
    pass


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        run()
