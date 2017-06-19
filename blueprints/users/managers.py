from werkzeug.security import generate_password_hash, check_password_hash
from ..database import mongo


class UserManager(object):
    @staticmethod
    def create_user(data):
        user = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': generate_password_hash(data.get('password')),
        }
        return mongo.db.users.insert_one(user).inserted_id

    @staticmethod
    def delete_user(username):
        mongo.db.users.remove({'username': username})

    @staticmethod
    def check_auth(username, password):
        user = mongo.db.users.find_one({'username': username})
        return (user and check_password_hash(user['password'], password))

    @staticmethod
    def is_username_exists(username):
        users = mongo.db.users.find({'username': username})
        return bool(users.count())
