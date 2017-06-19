from flask import Blueprint

blueprint = Blueprint('landingpage', __name__)


@blueprint.route('/')
def homepage():
    return 'This is the homepage.'
