from wtforms import (
    Form, StringField, PasswordField, validators, ValidationError
)


class RegisterForm(Form):
    username = StringField('Username', [
        validators.Length(min=3, max=25),
    ])
    email = StringField('Email', [
        validators.Email(),
    ])
    password = PasswordField('New password', [
        validators.InputRequired(),
        validators.EqualTo('confirm_password', message='Both password must match.'),
    ])
    confirm_password = PasswordField('Repeat password', [
        validators.InputRequired(),
    ])


class LoginForm(Form):
    username = StringField('Username', [
        validators.InputRequired(),
    ])
    password = PasswordField('Password', [
        validators.InputRequired(),
    ])
