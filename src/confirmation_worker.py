#!/usr/bin/env python
# encoding: utf-8

import os
from contextlib import suppress
from steem.blockchain import Blockchain
from .methods import db, send_mail, send_telegram

steem_wallet = os.getenv('STEEM_WALLET', 'furion')


def run():
    print('Starting the confirmation worker.')
    for op in b.stream():
        if op['type'] == 'transfer':
            confirm_user_settings(op)


def confirm_user_settings(op):
    try:
        to = op['to']
        asset = op['amount']['asset']
        amount = op['amount']['amount']
    except KeyError:
        return
    if asset != 'STEEM' or amount != 0.001 or to != steem_wallet:
        return
    print('Received confirmation from: %s.' % op['from'])
    db.settings.update_one(
        {'_id': op['memo'], 'username': op['from']}, 
        {'$set': {'confirmed': True}}
    )
    settings = db.settings.find_one({'_id': op['memo']})
    message = 'You have made the following changes:\n' + \
              'Email: %s\n' % (str(settings['email'] or '-')) + \
              'Telegram: %s\n' % (str(settings['telegram_channel_id'] or '-')) + \
              'Notify account_update: %s\n' % str(settings['account_update']) + \
              'Notify change_recovery_account: %s\n' % str(settings['change_recovery_account']) + \
              'Notify request_account_recovery: %s\n' % str(settings['request_account_recovery']) + \
              'Notify transfer: %s\n' % str(settings['transfer']) + \
              'Notify transfer_from_savings: %s\n' % str(settings['transfer_from_savings']) + \
              'Notify set_withdraw_vesting_route: %s\n' % str(settings['set_withdraw_vesting_route']) + \
              'Notify withdraw_vesting: %s\n' % str(settings['withdraw_vesting']) + \
              'Notify fill_order: %s\n' % str(settings['fill_order']) + \
              'Notify fill_convert_request: %s\n' % str(settings['fill_convert_request']) + \
              'Notify fill_transfer_from_savings: %s\n' % str(settings['fill_transfer_from_savings']) + \
              'Notify fill_vesting_withdraw: %s\n' % str(settings['fill_vesting_withdraw'])
    if settings['email']:
        send_mail(settings['email'], 'Update confirmed', message)
    if settings['telegram_channel_id']:
        send_telegram(settings['telegram_channel_id'], message)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        run()
