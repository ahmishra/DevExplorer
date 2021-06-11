import bcrypt
# Other Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# GLOBAL APP VARIABLES
app = Flask(__name__)
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Extentions
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)


# Importing Routes
from main import routes
