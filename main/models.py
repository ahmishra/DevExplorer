from datetime import datetime
from main import db, login_manager
from flask_login import UserMixin


# User Loader, for login page
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Model To Store Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.id}, {self.username})"


# Post Model For Storing User's Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=False, default="https://designshack.net/wp-content/uploads/placeholder-image.png")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post({self.id}, {self.title}, {self.date_posted})"
