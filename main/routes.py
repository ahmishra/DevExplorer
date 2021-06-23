# Imports
from flask_login.utils import login_required, login_user, current_user, logout_user
from werkzeug.wrappers import request
from main.models import User, Post
from flask import render_template, redirect, url_for, flash, abort, request
from main.forms import RegistrationForm, LoginForm, NewPostForm, ResetPWDForm, RequestResetPWDForm
from main import app, bcrypt, db, news_scraper, mail
from flask_mail import Message


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
		user = User(username=form.username.data, password=hashed_pwd, email=form.email.data)
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



# Request Reset Password Form
@app.route("/passwordreset", methods=["GET", "POST"])
def request_reset_pwd():
	if current_user.is_authenticated:
		flash("You are already logged in please log out first", "warning")
		return redirect(url_for('home'))

	form = RequestResetPWDForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email was sent to your inbox, please follow the instructions inside of it to reset your password!", "info")
		return redirect(url_for('login'))

	return render_template("request_reset_password.html", form=form)



# Reset Password Form
@app.route("/passwordreset/<token>", methods=["GET", "POST"])
def reset_pwd(token):
	if current_user.is_authenticated:
		flash("You are already logged in please log out first", "warning")
		return redirect(url_for('home'))

	user = User.verify_reset_token(token=token)

	if user is None:
		flash("The token that you provided is maybe invalid or is expired", "warning")
		return redirect(url_for("request_reset_pwd"))

	form = ResetPWDForm()

	# Adding User To Database Once Submitted
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pwd
		db.session.commit()
		flash(f"Your password was changed successfully, You may now login!", "success")
		return redirect(url_for('login'))

	return render_template("reset_token.html", form=form)



# Email Sender
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("DevExplorer- Reset Your Password",
	              sender="devexplorerh1@gmail.com", recipients=[user.email])
	msg.body = f"""DevExplorer - Reset Your Password:\n
To reset your password please visit this link {url_for('reset_pwd', token=token, _external=True)}

If you didn't make this request simply, ignore or delete this email!
	"""

	mail.send(msg)





"""
Main juice of the project
"""

# DevNews
@app.route("/devnews")
def devnews():
	news=news_scraper.return_news()
	return render_template("devnews.html", news=news)



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
