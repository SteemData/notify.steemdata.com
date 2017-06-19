from flask_testing import TestCase
from blueprints.database import mongo
from blueprints.users.managers import UserManager
from app import create_app


class BaseTests(TestCase):
    def create_app(self):
        self.app = create_app(testing=True)
        return self.app

    def setUp(self):
        self.bob = UserManager.create_user({
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 's3cr3t',
        })
        self.alice = UserManager.create_user({
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 's3cr3t',
        })
        self.mongo = mongo

    def tearDown(self):
        self.mongo.db.users.delete_many({})

    def login(self, username, password):
        return self.client.post('/users/login', data={
            'username': username,
            'password': password,
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/users/logout', follow_redirects=True)
