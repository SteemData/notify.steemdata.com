from flask import Blueprint, render_template, redirect, session, url_for

blueprint = Blueprint('landingpage', __name__)


@blueprint.route('/')
def homepage():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    return render_template('landingpage/home.html', username=session['username'])
