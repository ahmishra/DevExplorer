from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from main.models import User

# Form To Make The User Registered
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    password_confirm = PasswordField("Confirm Password", validators=[
                             DataRequired(), Length(min=8, max=64), EqualTo('password')])

    submit = SubmitField('Register')

    # Custom Validator
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken, please choose another one.")

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')


# New Post Form
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(3)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(3)])
    thumbnail = StringField('Thumbnail(Image URL)', validators=[DataRequired(), Length(3)])
    submit = SubmitField('Post')
