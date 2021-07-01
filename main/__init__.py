"""
Heart of the app :)

PYLINT: 9.80/10
"""


# Other Imports / Extentions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.markdown import Markdown
from flask_mail import Mail
from newsapi import NewsApiClient
import newsapi


# Main App
app = Flask(__name__)

# GLOBAL APP VARIABLES
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 0000
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'devexplorerh1@gmail.com'
app.config['MAIL_PASSWORD'] = "explorer11thousand"


# Extentions
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
md = Markdown(app, output_format='html5', extensions=["fenced_code"])
mail = Mail(app=app)
newsapi = newsapi.NewsApiClient(api_key="eb222d46c8b8446987ecccd93d7edf8b")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Importing Routes (AT THE END TO AVOID CIRCULAR IMPORTS)
from main import routes
