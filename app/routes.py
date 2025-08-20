from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignupForm, CreatePostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.database import User, load_user, add_user, get_connection, user_exists, add_post
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    conn.close()
    return render_template('index.html', reviews=reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = get_connection()
    cursor = conn.cursor()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute("SELECT * FROM users WHERE username = (?)", [form.username.data])
        user_data = list(cursor.fetchone())
        loaded_user = load_user(user_data[0])

        if user_data is None:
            flash("Invalid User Credentials")
            return redirect(url_for('login'))
        
        if (form.username.data == user_data[1]) and (form.password.data == user_data[3]):
            login_user(loaded_user, remember=form.remember_me.data)

        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if user_exists(form.username.data, form.email.data):
            flash("Email or Username taken")
        else:
            add_user(form.username.data, form.email.data, form.password.data)
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_review():
    form = CreatePostForm()
    if form.validate_on_submit():
        add_post(current_user.id, form.plate.data, form.description.data, form.rating.data)
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/user/<user_id>')
def users(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = (?)", [user_id])
    user_data = cursor.fetchone()

    cursor.execute("SELECT * FROM reviews WHERE author_id = (?)", [user_id])
    reviews = cursor.fetchall()
    print(reviews)

    return render_template('user.html', user_data=user_data, reviews=reviews)

@app.route('/plate/<plate>')
def plates(plate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews WHERE plate = (?)", [plate])
    reviews = cursor.fetchall()
    print(reviews)

    return render_template('plate.html', reviews=reviews)

@app.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    return redirect(url_for('users', user_id=user_id))



# Error Handlers

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500