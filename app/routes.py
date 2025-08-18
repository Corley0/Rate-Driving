from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignupForm

@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            "post_id": 0,
            "plate": "Test One",
            "author": {"user_id": 0, "username": "Corley"},
            "body": "Good driver",
            "rating": 5
        },
        {
            "post_id": 1,
            "plate": "Test Two",
            "author": {"user_id": 1, "username": "Corley2"},
            "body": "Bad Driver",
            "rating": 0
        }
    ]
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/index'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup requested for user {}, email={}, password={}'.format(
            form.username.data, form.email.data, form.password.data))
        return redirect(url_for('/index'))
    return render_template('signup.html', form=form)