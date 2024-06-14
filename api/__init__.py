from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .orders.views import order_namespace


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(order_namespace, path='/')
    app.config['SECRET_KEY'] = 'XXXXXX'

    return app
