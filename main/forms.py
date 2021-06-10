from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    password_confirm = PasswordField("Confirm Password", validators=[
                             DataRequired(), Length(min=8, max=64), EqualTo('password')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8, max=64)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')
