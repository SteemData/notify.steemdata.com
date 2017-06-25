#!/usr/bin/env python
# encoding: utf-8

import os
from contextlib import suppress
from steem.blockchain import Blockchain
import requests
from pymongo import MongoClient


mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/steem_notifier')
telegram_token = os.getenv('TELEGRAM_TOKEN')
mailgun_domain_name = os.getenv('MAILGUN_DOMAIN_NAME')
mailgun_api_key = os.getenv('MAILGUN_API_KEY')

client = MongoClient(mongo_uri)
db = client[mongo_uri.split('/')[-1]]


def run():
    print('Starting the Steem event listener.')
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
        if operation['type'] == 'transfer':
            handle_transfer(operation)


def handle_transfer(op):
    settings = db.settings.find_one({'username': op['from']})
    if settings and settings['transfer']:
        message = 'Received event: transfer\nEvent detail: %s -> %s (%s)' % (
            op['from'], op['to'], op['amount'],
        )
        if settings['email']:
            send_mail(settings['email'], 'New Steem Event', message)
        if settings['telegram_channel_id']:
            send_telegram(settings['telegram_channel_id'], message)
        db.processed_blockchains.insert_one(op)


def send_mail(to, subject, message):
    url = 'https://api.mailgun.net/v3/%s/messages' % mailgun_domain_name 
    auth = {'api': mailgun_api_key}
    data = {
        'from': 'noreply@%s' % mailgun_domain_name,
        'to': [to],
        'subject': subject,
        'text': message,
    }
    try:
        requests.post(url, auth=auth, data=data)
        print('Sent mail to: %s.' % to)
    except Exception:
        print('Failed sending email to: %s.' % to)


def send_telegram(channel_id, message):
    url = 'https://api.telegram.org/bot%s/sendMessage' % telegram_token
    try:
        data = {'chat_id': channel_id, 'text': message}
        r = requests.post(url, data=data)
        print('Sent notification to: %s.' % channel_id)
    except Exception:
        print('Failed sending telegram message to: %s.' % channel_id)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        run()
