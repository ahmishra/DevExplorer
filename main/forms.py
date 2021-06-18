from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, FloatField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, ValidationError
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


# Lat, Long
class GetFieldForm(FlaskForm):
    field_name = StringField('Designation')
    field_latitude = FloatField('Latitude', default=-30, validators=[InputRequired()], description='48.182601')
    field_longitude = FloatField('Longitude', default=150, validators=[InputRequired()], description='11.304939')
    submit = SubmitField('Search')
