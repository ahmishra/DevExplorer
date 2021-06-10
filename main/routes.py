from flask import request, render_template, redirect, url_for, flash
from main import app

@app.route("/")
def home():
	return render_template("index.html")
