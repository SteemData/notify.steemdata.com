from flask import Blueprint, render_template

blueprint = Blueprint('users', __name__)

@blueprint.route('/login')
def login():
    return render_template('users/login.html')
