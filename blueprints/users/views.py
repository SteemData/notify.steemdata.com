from flask import (
    Blueprint, Response, session,
    request, render_template, flash, redirect
)
from .managers import UserManager
from .forms import RegisterForm, LoginForm


blueprint = Blueprint('users', __name__)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        UserManager.create_user(form.data)
        session['username'] = form.username.data
        return redirect('/')
    return render_template('users/register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            if UserManager.check_auth(username, password):
                session['username'] = username
                return redirect('/')
            error = 'Invalid username/password'
    return render_template('users/login.html', form=form, error=error)


@blueprint.route('/logout')
def logout():
    del session['username']
    return redirect('/users/login')
