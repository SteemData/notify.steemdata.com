import os
import requests
from pymongo import MongoClient


mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/steem_notifier')
telegram_token = os.getenv('TELEGRAM_TOKEN')
mailgun_domain_name = os.getenv('MAILGUN_DOMAIN_NAME')
mailgun_api_key = os.getenv('MAILGUN_API_KEY')

client = MongoClient(mongo_uri)
db = client[mongo_uri.split('/')[-1]]


def find_user_settings(username):
    try:
        rows = db.settings.find({'username': username, 'confirmed': True}).sort('created_at', -1)
        return rows[0]
    except Exception:
        return dict()


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

