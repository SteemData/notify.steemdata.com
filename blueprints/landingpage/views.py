from flask import Blueprint, redirect, url_for

blueprint = Blueprint('landingpage', __name__)


@blueprint.route('/')
def homepage():
    return redirect(url_for('users.login'))
