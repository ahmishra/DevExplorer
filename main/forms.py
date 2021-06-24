"""
File to render app forms

PYLINT: 10/10
"""


# Imports
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from main.models import User



# Form To Make The User Registered
class RegistrationForm(FlaskForm):

    """
    :params: none
    :inherits:FlaskForm, wtforms

    Form for the registration page
    """

    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Length(min=3, max=1000)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=64)])
    password_confirm = PasswordField("Confirm Password",
        validators=[DataRequired(), Length(min=8, max=64), EqualTo('password')])

    submit = SubmitField('Register')

    # Custom Validators
    def validate_username(self, username):

        """
        :params: username:to validate it

        Validates the username of a specific user that it is unique
        """

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken, please choose another one.")

    def validate_email(self, email):


        """
        :params: email:to validate it

        Validates the email of a specific user that it is unique
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken, please choose another one.")



# Login Form
class LoginForm(FlaskForm):

    """
    :params: none
    :inherits:FlaskForm, wtforms

    Form for the login page
    """

    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')



# New Post Form
class NewPostForm(FlaskForm):

    """
    :params: none
    :inherits:FlaskForm, wtforms

    Form for to make a new post
    """

    title = StringField('Title', validators=[DataRequired(), Length(3)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(3)])
    thumbnail = StringField('Thumbnail(Image URL)', validators=[DataRequired(), Length(3)])
    submit = SubmitField('Post')



# Request A Password Reset Form
class RequestResetPWDForm(FlaskForm):

    """
    :params: none
    :inherits:FlaskForm, wtforms

    Form for to request a password reset
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):


        """
        :params: email:to validate it

        Validates the email of a specific user that it is unique
        """

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



# Password Reset Form
class ResetPWDForm(FlaskForm):

    """
    :params: none
    :inherits:FlaskForm, wtforms

    Form for resetting password
    """

    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    password_confirm = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=8, max=64), EqualTo('password')])

    submit = SubmitField("Reset Password")
