from flask import (
    Blueprint, request, render_template, flash, redirect,
)
from .forms import RegisterForm, LoginForm

blueprint = Blueprint('users', __name__)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('users/register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Invalid username/password', 'danger')
        return redirect('/users/login')
    return render_template('users/login.html', form=form)
