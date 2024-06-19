from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description='A namespace for authentication')

@auth_namespace.route('/signup')
class SignUp(Resource):
    """
    SignUp namespace
    """
    def post(self):
        """
        Create a new user account
        """
        pass

@auth_namespace.route('/login')
class Login(Resource):
    """
    Login namespace
    """
    def post(self):
        """
        Authenticate a user and generate an access token
        """
        pass