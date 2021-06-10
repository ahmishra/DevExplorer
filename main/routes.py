from re import LOCALE
from flask import request, render_template, redirect, url_for, flash
from main import app
from main.forms import RegistrationForm, LoginForm

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/register")
def register():
	form = RegistrationForm()
	return render_template("register.html", form=form)


@app.route("/login")
def login():
	form = LoginForm()
	return render_template("login.html", form=form)
