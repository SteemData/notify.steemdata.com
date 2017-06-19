from flask_testing import TestCase
from blueprints.database import mongo
from app import create_app


class BaseTests(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        self.mongo = mongo
    