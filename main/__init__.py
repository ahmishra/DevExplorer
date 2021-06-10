from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"

from main import routes
