from wtforms import (
    Form, StringField, PasswordField, validators, ValidationError
)
from .managers import UserManager


class RegisterForm(Form):
    username = StringField('Username', [
        validators.InputRequired(),
        validators.Length(min=3, max=25),
    ])
    email = StringField('Email', [
        validators.InputRequired(),
        validators.Email(),
    ])
    password = PasswordField('New password', [
        validators.InputRequired(),
        validators.EqualTo('confirm_password', message='Both password must match.'),
    ])
    confirm_password = PasswordField('Confirm password', [
        validators.InputRequired(),
    ])

    def validate_username(self, field):
        if UserManager.is_username_exists(field.data):
            raise ValidationError('This username is already taken.')


class LoginForm(Form):
    username = StringField('Username', [
        validators.InputRequired(),
    ])
    password = PasswordField('Password', [
        validators.InputRequired(),
    ])
