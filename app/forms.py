from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Field must not be empty")])
    password = PasswordField('Password', validators=[DataRequired("Field must not be empty")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Field must not be empty")])
    email = StringField('Email Address', validators=[DataRequired("Field must not be empty"), Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired("Field must not be empty")])
    rewrite_password = PasswordField('Rewrite Password', validators=[DataRequired("Field must not be empty")])
    submit = SubmitField('Sign In')