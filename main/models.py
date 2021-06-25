"""
File that contains / makes models / databases for our app

PYLINT: 10/10
"""

# Imports
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main import db, login_manager, app


# User Loader, for login page
@login_manager.user_loader
def load_user(user_id):

    """
    :params: user_id, to load the user in with that id

    Returns the user from the database

    """

    return User.query.get(int(user_id))



# User Model To Store Users
class User(db.Model, UserMixin):

    """
    :params: none
    :inherits: db.Model, UserMixin

    Database model to store users
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)


    # Reset Password For User
    def get_reset_token(self, expires_sec=1800):

        """
        :params: expires_sec:seconds for the token to expire

        Gets the reset token for a specific user after a specific amount of time
        the user token will be deleted / expired, and it wont work
        """

        serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):

        """
        :params: token:to validate the of the token
        Verifies if the given token is valid or not
        """

        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except ValueError:
            return None
        return User.query.get(user_id)



    def __repr__(self):

        """
        :params: none
        Displays useful infortmation when a class is printed
        """

        return f"User({self.username}, {self.id})"



# Post Model For Storing User's Posts
class Post(db.Model):

    """
    :params: none
    :inherits: db.Mode

    Database model to store user's posts
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(
        db.String(1000),
        nullable=False,
        default="https://designshack.net/wp-content/uploads/placeholder-image.png"
    )

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):

        """
        :params: none
        Displays useful infortmation when a class is printed
        """

        return f"Post({self.title}, {self.date_posted}, {self.id})"
