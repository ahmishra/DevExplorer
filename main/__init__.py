from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

from main import routes
