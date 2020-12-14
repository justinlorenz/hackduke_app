from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    remember = True if request.form.get('remember') else False

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Your username or password were not correct')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    location = request.form.get('location')
    mentor = True if request.form.get('mentor') else False

    if (User.query.filter_by(email=email).first()) or (User.query.filter_by(username=username).first()):
        flash('Email or Username already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'),
                    location=location, mentor=mentor, prefs="")

    db.session.add(new_user)
    db.session.commit()

    session['username'] = username

    return redirect(url_for('auth.signup_preferences'))


@auth.route('/signup_preferences')
def signup_preferences():
    return render_template('signup_preferences.html')


@auth.route('/signup_preferences', methods=['POST'])
def signup_preferences_post():
    pref_string = ""
    for i in range(5):
        prefNumber = "pref" + "" + str(i)
        if i == 4:
            pref_string += request.form.get(prefNumber)
        else:
            pref_string += request.form.get(prefNumber) + ","
    username = session.pop('username', None)
    new_user = User.query.filter_by(username=username).first()

    new_user.prefs = pref_string

    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


