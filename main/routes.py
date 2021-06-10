from re import LOCALE
from flask import request, render_template, redirect, url_for, flash
from main import app
from main.forms import RegistrationForm, LoginForm
# from main.models import
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app=app)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f"Registration Was Succesful For {form.username.data}!", "success")
		return redirect(url_for('home'))
	return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f"Login Was Succesful For {form.username.data}!", "success")
		return redirect(url_for('home'))
	else:
		flash("Login Unsuccesful, Please Check your credentials", "danger")
	return render_template("login.html", form=form)
