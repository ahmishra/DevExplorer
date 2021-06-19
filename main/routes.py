# Imports
from flask_login.utils import login_required, login_user, current_user, logout_user
from werkzeug.wrappers import request
from main.models import User, Post
from flask import render_template, redirect, url_for, flash, abort, request
from main.forms import RegistrationForm, LoginForm, NewPostForm
from main import app, bcrypt, db, ScrapeNews
import xlrd

# Major bug fixing line, (elementtree has not attr getiterator) caused by python 3.9+
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True


# Home Page
@app.route("/")
def home():
	return render_template("index.html")


"""
User Authentication
"""


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



"""
Main juice of the project
"""

# DevNews
@app.route("/devnews")
def devnews():
	ScrapeNews().scrape()
	excel_file = ("main\\TechCrunch_latest_news.xlsx")
	wb = xlrd.open_workbook(excel_file)
	sheet = wb.sheet_by_index(0)
	return render_template("devnews.html", sheet=sheet, cols=[i for i in range(sheet.nrows)])



# Map
@app.route("/map", methods=["GET", "POST"])
def map():
	mapbox_token = "pk.eyJ1IjoiYXJ5YW5taXNocmEiLCJhIjoiY2txMHZjenYzMDdvOTJ2cDg5eGd6YXJmYiJ9.fYTdLFatoaLwFzx4R9z9nA"
	return render_template('map.html', mapbox_access_token=mapbox_token)



# Blog(List)
@app.route("/posts")
def list_posts():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(
		Post.date_posted.desc()).paginate(page=page, per_page=6)
	return render_template("posts.html", posts=posts)



# Blog(New)
@app.route("/posts/new", methods=["POST", "GET"])
@login_required
def new_post():
	form = NewPostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data,
		            content=form.content.data, thumbnail=form.thumbnail.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f"{post.title} was created!", "info")
		return redirect(url_for('post_detail', pk=post.id))

	return render_template("new-post.html", form=form)



# Blog(Detail)
@app.route("/post/<int:pk>")
def post_detail(pk):
	post = Post.query.get_or_404(pk)
	return render_template('post-detail.html', post=post)



# Blog(Update)
@app.route("/post/<int:pk>/update", methods=["POST", "GET"])
@login_required
def post_update(pk):
	post = Post.query.get_or_404(pk)
	if post.author != current_user:
		abort(403)

	form = NewPostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		post.thumbnail = form.thumbnail.data
		db.session.commit()
		flash("Your Post, Has Been Updated!", "success")
		return redirect(url_for('post_detail', pk=post.id))

	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content
		form.thumbnail.data = post.thumbnail

	return render_template('post-update.html', form=form)



# Blog(Delete)
@app.route("/post/<int:pk>/delete", methods=["POST", "GET"])
@login_required
def post_delete(pk):
	post = Post.query.get_or_404(pk)
	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash("Your Post, Has Been Deleted!", "success")
	return redirect(url_for('list_posts'))



# Credits ;)
@app.route("/credits")
def credits():
	return render_template("credits.html")
