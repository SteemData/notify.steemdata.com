#!/usr/bin/env python
# encoding: utf-8

import re
import os

from flask import Flask, request, render_template, redirect, flash
from flask_pymongo import PyMongo
from wtforms import (
    Form, StringField, BooleanField, validators, ValidationError,
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = '0123456789abcdef'
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/steem_notifier')
app.config['DEBUG'] = not os.getenv('PRODUCTION', False)
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


class NotificationSettingsForm(Form):
    email = StringField('Email', [validators.Optional(), validators.Email()])
    telegram_channel_id = StringField('Telegram Channel ID')
    account_update = BooleanField('Account update')
    change_recovery_account = BooleanField('Change recovery account')
    request_account_recovery = BooleanField('Request account recovery')
    transfer = BooleanField('Transfer')
    transfer_from_savings = BooleanField('Transfer from savings')
    set_withdraw_vesting_route = BooleanField('Set withdraw vesting route')
    withdraw_vesting = BooleanField('Withdraw vesting')
    fill_order = BooleanField('Fill order')
    fill_convert_request = BooleanField('Fill convert request')
    fill_transfer_from_savings = BooleanField('Fill transfer from savings')
    fill_vesting_withdraw = BooleanField('Fill vesting withdraw')

    def validate_telegram_channel_id(self, field):
        if field.data and not re.match('^@[a-zA-Z0-9]+$', field.data):
            raise ValidationError('Wrong format for telegram channel ID.')


@app.route('/<username>', methods=['GET', 'POST'])
def settings(username):
    form = NotificationSettingsForm(
        request.form, 
        data=mongo.db.settings.find_one({'username': username}),
    )
    if request.method == 'POST' and form.validate():
        data = form.data
        data['username'] = username
        mongo.db.settings.update({'username': username}, data, upsert=True)
        flash('Successfully saved new settings for %s.' % username)
        return redirect('/%s' % username)
    return render_template('settings.html', username=username, form=form)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
