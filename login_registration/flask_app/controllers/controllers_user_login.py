from flask_app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User
from werkzeug.security import check_password_hash

@app.route('/')
def index():
    return redirect('/main_page')

@app.route('/main_page')
def main_page():

    messages = get_flashed_messages(with_categories=True)

    return render_template('index.html', messages=messages)


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']


    if len(first_name) < 2:
        flash("First name must be at least 2 characters", "register_error")
    if len(last_name) < 2:
        flash("Last name must be at least 2 characters", "register_error")
    if not User.find_by_email(email):
        flash("Invalid email format or email already exists", "register_error")
    if len(password) < 8:
        flash("Password must be at least 8 characters", "register_error")
    if password != confirm_password:
        flash("Password and confirmation do not match", "register_error")


    if '_flashes' in session:
        return redirect(url_for('main_page'))


    User.create(first_name, last_name, email, password)
    flash("Registration successful!", "success")
    return redirect(url_for('main_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.find_by_email(email)
    if user and check_password_hash(user.password_hash, password):
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        flash(f"Logged in as {user.first_name} {user.last_name}", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid email or password", "login_error")
        return redirect(url_for('main_page'))

@app.route('/dashboard')
def dashboard():
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    return render_template('success.html', first_name=first_name, last_name=last_name)



