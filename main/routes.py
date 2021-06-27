"""

Routes / URLs for the app to render in,
when the user requests a URL such as localhost:5000/home

PYLINT: 9.83/10
"""


# Imports
from flask_login.utils import login_required, login_user, current_user, logout_user
from flask import render_template, redirect, url_for, flash, abort, request
from flask_mail import Message
from main.models import User, Post
from main.forms import RegistrationForm, LoginForm, NewPostForm, ResetPWDForm, RequestResetPWDForm
from main import app, bcrypt, db, news_scraper, mail



# Home Page
@app.route("/")
def home():
    """
    :params: none
    A simple home page...
    """
    return render_template("index.html")



#### User Auth #####



# Register Page
@app.route("/register", methods=["POST", "GET"])
def register():

    """
    :params: none
    Displays a HTML Form, when submitted checks if the
    values are valid, then adds the value to the database.
    """

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

    """
    :params: none
    Displays a HTML Form, when submitted checks if the
    values are valid, then checks the credentials from the database,
    if the credentials are correct, the user logs in

    """

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

    """
    :params: none
    Calls a built-in function, and logs the user out

    """

    logout_user()
    return redirect(url_for('home'))



# Request Reset Password Form
@app.route("/passwordreset", methods=["GET", "POST"])
def request_reset_pwd():

    """
    :params: none
    Displays a HTML Form, when submitted checks if the
    values are valid, then checks if the email exists in
    the database, if yes sends an email with a token to
    reset their password
    """

    if current_user.is_authenticated:
        flash("You are already logged in please log out first", "warning")
        return redirect(url_for('home'))

    form = RequestResetPWDForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email was sent to your inbox, \
            please follow the instructions inside of it to reset your password!", "info")
        return redirect(url_for('login'))

    return render_template("request_reset_password.html", form=form)



# Reset Password Form
@app.route("/passwordreset/<token>", methods=["GET", "POST"])
def reset_pwd(token):

    """
    :params: none
    Displays an HTML Form, validates the password,
    if they are correct, resets the User's password

    """

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
        flash("Your password was changed successfully, You may now login!", "success")
        return redirect(url_for('login'))

    return render_template("reset_token.html", form=form)



# Email Sender
def send_reset_email(user):

    """
    :params: none
    Sends the email to the user with a token to reset their password

    """

    token = user.get_reset_token()
    msg = Message("DevExplorer- Reset Your Password",
                  sender="umasaryan@gmail.com", recipients=[user.email])
    msg.body = f"""DevExplorer - Reset Your Password:\n
To reset your password please visit this link {url_for('reset_pwd', token=token, _external=True)}\n

If you didn't make this request simply, ignore or delete this email!
                """


    mail.send(msg)



#### Main Content ####



# DevNews
@app.route("/devnews")
def devnews():

    """
    :params: none
    Renders in the news

    """

    news=news_scraper.return_news()
    return render_template("devnews.html", news=news)



# Map
@app.route("/map", methods=["GET", "POST"])
def map_render():

    """
    :params: none
    Renders in the map

    """

    mapbox_token = "pk.eyJ1IjoiYXJ5YW5taXNocmEiLCJhIjoiY2txMHZjenYz\
MDdvOTJ2cDg5eGd6YXJmYiJ9.fYTdLFatoaLwFzx4R9z9nA"
    return render_template('map.html', mapbox_access_token=mapbox_token)



# Blog(List)
@app.route("/posts")
def list_posts():

    """
    :params: none
    Lists all of the posts inside of the database

    """

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=6)

    return render_template("posts.html", posts=posts)



# Blog(New)
@app.route("/posts/new", methods=["POST", "GET"])
@login_required
def new_post():

    """
    :params: none
    Displays a HTML Form, when submitted checks if the
    values are valid, then adds the post to the database

    """

    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, thumbnail=form.thumbnail.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f"{post.title} was created!", "info")
        return redirect(url_for('post_detail', primary_key=post.id))

    return render_template("new-post.html", form=form)



# Blog(Detail)
@app.route("/post/<int:primary_key>")
def post_detail(primary_key):

    """
    :params: primart key
    Displays a detailed view of a post

    """

    post = Post.query.get_or_404(primary_key)
    return render_template('post-detail.html', post=post)



# Blog(Update)
@app.route("/post/<int:primary_key>/update", methods=["POST", "GET"])
@login_required
def post_update(primary_key):

    """
    :params: primart key
    Displays a HTML Form, when submitted checks if the
    values are valid, then updates the post in the database
    if the author of the post is not the current user simply
    aborts the operation

    """

    post = Post.query.get_or_404(primary_key)
    if post.author != current_user:
        abort(403)


    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.thumbnail = form.thumbnail.data
        db.session.commit()
        flash("Your Post, Has Been Updated!", "success")
        return redirect(url_for('post_detail', primary_key=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.thumbnail.data = post.thumbnail

    return render_template('post-update.html', form=form)



# Blog(Delete)
@app.route("/post/<int:primary_key>/delete", methods=["POST", "GET"])
@login_required
def post_delete(primary_key):

    """
    :params: primart key
    Displays a HTML Form, when submitted checks if the
    values are valid, then delets the post in the database
    if the author of the post is not the current user simply
    aborts the operation

    """

    post = Post.query.get_or_404(primary_key)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Your Post, Has Been Deleted!", "success")
    return redirect(url_for('list_posts'))



# Credits ;)
@app.route("/credits")
def credits_page():

    """
    ^_^ some cheeky credits, I suppose...
    """

    return render_template("credits.html")
