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
    for op in b.stream():
        processed = db.processed_blockchains.find_one({'_id': op['_id']}).count()
        if op['type'] in types and not processed:
            parse_blockchain(op)
            db.processed_blockchains.insert_one(op)


def parse_blockchain(op):
    settings = None
    message = None

    if op['type'] == 'account_update':
        settings = db.settings.find_one({'username': op['account']})
        if settings and settings['account_update']:
            message = 'Received event: account_update (%s)' % op['account']

    elif op['type'] in ['transfer', 'transfer_from_savings']:
        settings = db.settings.find_one({'username': op['from']})
        if settings and settings[op['type']]:
            message = 'Received event: %s\nEvent detail: %s -> %s (%s)' % (
                op['type'], op['from'], op['to'], op['amount'],
            )

    elif op['type'] == 'withdraw_vesting':
        settings = db.settings.find_one({'username': op['account']})
        if settings and settings['withdraw_vesting']:
            message = 'Received event: %s\nAccount: %s\nVesting shares: %s' % (
                op['type'], op['account'], op['vesting_shares']
            )

    elif op['type'] == 'fill_order':
        settings = db.settings.find_one({'username': op['current_owner']})
        if settings and settings['fill_order']:
            message = "Received event: fill_order\n" + \
                      "Current owner: %s\n" % (op['current_owner']) + \
                      "Current pays: %s\n" % (op['current_pays']) + \
                      "Open owner: %s\n" % (op['open_owner']) + \
                      "Open pays: %s" % (op['open_pays']) 

    elif op['type'] == 'fill_convert_request':
        settings = db.settings.find_one({'username': op['owner']})
        if settings and settings['fill_convert_request']:
            message = 'Received event: fill_convert_request\n' + \
                      'Owner: %s\n' % op['owner'] + \
                      'Amount in: %s\n' % op['amount_in'] + \
                      'Amount out: %s' % op['amount_out']

    elif op['type'] == 'fill_transfer_from_savings':
        settings = db.settings.find_one({'username': op['from']})
        if settings and settings['fill_transfer_from_savings']:
            message = 'Received event: fill_transfer_from_savings\n' + \
                      'From: %s\n' % op['from'] + \
                      'To: %s\n' % op['to'] + \
                      'Amount: %s' % op['amount']

    elif op['type'] == 'fill_vesting_withdraw':
        settings = db.settings.find_one({'username': op['from_account']})
        if settings and settings['fill_vesting_withdraw']:
            message = 'Received event: fill_vesting_withdraw\n' + \
                      'From account: %s\n' % op['from_account'] + \
                      'To account: %s\n' % op['to_account'] + \
                      'Withdrawn: %s\n' % op['withdrawn'] + \
                      'Deposited: %s' % op['deposited']

    elif op['type'] == 'set_withdraw_vesting_route':
        settings = db.settings.find_one({'username': op['from_account']})
        if settings and settings['set_withdraw_vesting_route']:
            message = 'Received event: set_withdraw_vesting_route\n' + \
                      'From account: %s\n' % op['from_account'] + \
                      'To account: %s\n' % op['to_account'] + \
                      'Percent: %s' % op['percent']

    elif op['type'] == 'change_recovery_account':
        settings = db.settings.find_one({'username': op['account_to_recover']})
        if settings and settings['change_recovery_account']:
            message = 'Received event: change_recovery_account\n' + \
                      'Account to recover: %s\n' % op['account_to_recover'] + \
                      'New recovery account: %s' % op['new_recovery_account']

    elif op['type'] == 'request_account_recovery':
        settings = db.settings.find_one({'username': op['account_to_recover']})
        if settings and settings['request_account_recovery']:
            message = 'Received event: request_account_recovery\n' + \
                      'Account to recover: %s\n' % op['account_to_recover'] + \
                      'Recovery account: %s' % op['recovery_account']

    if settings and message:
        if settings['email']:
            send_mail(settings['email'], 'New Steem Event', message)
        if settings['telegram_channel_id']:
            send_telegram(settings['telegram_channel_id'], message)


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
