#!/usr/bin/env python
# encoding: utf-8

from contextlib import suppress
from steem.blockchain import Blockchain
import requests


telegram_token = '380184752:AAEObQIeG0ve_IVanUnR-p8GAdW9PRwVL_c'
chat_id = '@creativecoders'
users_to_watch = ['fnait', 'furion', 'flowfree']

def run():
    b = Blockchain()
    for op in b.stream():
        if op['type'] == 'transfer':
            print('%s -> %s (%s)' % (op['from'], op['to'], op['amount']))
            if op['from'] in users_to_watch:
                send_message('Payment successfully sent to %s.' % (op['to']))


def telegram(method, params=None):
    url = 'https://api.telegram.org/bot%s/%s' % (telegram_token, method)
    r = requests.post(url, data=params)
    return r.json()


def send_message(msg):
    params['chat_id'] = chat_id
    message = telegram('sendMessage', {'chat_id': chat_id, 'text': msg})
    if message.get('ok'):
        print('Notification sent to %s.' % chat_id)
    else:
        print('Failed sending message to %s.' % chat_id)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        run()
