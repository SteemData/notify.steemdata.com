#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from blueprints.landingpage.views import blueprint as landingpage_blueprint
from blueprints.users.views import blueprint as users_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = '0123456789abcdef'
    app.register_blueprint(landingpage_blueprint, url_prefix='/')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=3000, debug=True)
