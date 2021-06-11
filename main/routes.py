from flask_login.utils import login_user, current_user, logout_user
from main.models import User, Post
from flask import render_template, redirect, url_for, flash
from main.forms import RegistrationForm, LoginForm
from main import app, bcrypt, db


# Home Page
@app.route("/")
def home():
	return render_template("index.html")



# Register Page
@app.route("/register", methods=["POST", "GET"])
def register():
	if current_user.is_authenticated:
		flash("You are already logged in!", "warning")
		return redirect(url_for('home'))

	form = RegistrationForm()

	# Adding User To Database Once Submitted
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash(f"Registration Was Succesful For {form.username.data}, You can now login!", "success")
		return redirect(url_for('login'))
	
	return render_template("register.html", form=form)


# Login Page
@app.route("/login", methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		flash("You are already logged in!", "warning")
		return redirect(url_for('home'))

	form = LoginForm()

	# Validating User's Password And Username To That In The Database
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember_me.data)
			return redirect(url_for('home'))
		else:
			flash("Login Unsuccesful, Please Check your credentials", "danger")

	return render_template("login.html", form=form)


# Logging Out The User
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

