import unittest
from werkzeug.security import generate_password_hash
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.users import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_dict['test'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()



    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None
    
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password' : 'password'
        }
        response = self.client.post('/auth/signup', json= data)
        user = User.query.filter_by(email = "testuser@gmail.com").first()
        assert user.username == "testuser"

        assert response.status_code == 201

    def test_login(self):

        data = {
            "email" : "testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', data = data)

        assert response.status_code != 200