from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Field must not be empty")])
    password = PasswordField('Password', validators=[DataRequired("Field must not be empty")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Field must not be empty")])
    email = StringField('Email Address', validators=[DataRequired("Field must not be empty"), Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired("Field must not be empty"), EqualTo('rewrite_password', message='Passwords must match')])
    rewrite_password = PasswordField('Rewrite Password', validators=[DataRequired("Field must not be empty")])
    submit = SubmitField('Sign In')

class CreatePostForm(FlaskForm):
    plate = StringField('Registration Plate:', validators=[DataRequired("Field must not be empty"),Length(min=7,max=7, message="Must be a UK license plate")])
    description = TextAreaField('What happened?', render_kw={"rows": 10, "cols": 100}, validators=[DataRequired("Field must not be empty")])
    rating = IntegerField('Rating', validators=[DataRequired("Field must not be empty"), NumberRange(min=1, max=5, message="Must be  a value between 1 and 5 (inclusive)")])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search_input = StringField('Search', validators=[DataRequired("Field must not be empty"),Length(min=7,max=7, message="Must be a UK license plate")])
    submit = SubmitField('🔍')

class PunishForm(FlaskForm):
    PUNISH_TYPES = ['Delete Account', 'Delete Post', 'Promote', 'Demote']
    id = IntegerField('ID', validators=[DataRequired("Field must not be empty")])
    punish_type = SelectField('Punishments', choices=PUNISH_TYPES, validators=[DataRequired("Field must not be empty")])
    punish_type.choices = PUNISH_TYPES
    submit = SubmitField('Submit')