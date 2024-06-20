from ..utils import db

class User(db.Model):
    """
    User model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique=True)
    email = db.Column(db.String(45), nullable = False, unique=True)
    password_hash = db.Column(db.Text(), nullable = False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    orders =db.relationship('Order', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"