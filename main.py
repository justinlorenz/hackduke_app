from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from _csv import reader
from .models import User
from . import db
from .duke_API_course_finder import find_personal_courses

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    prefs = current_user.prefs.split(",")
    for pref in prefs:
        if pref == '':
            prefs.remove(pref)
    return render_template('dashboard.html', name=current_user.username, prefs=prefs)


@main.route('/mentors')
@login_required
def mentors():
    if current_user.mentor == True:
        print("You are a mentor urself")
        return redirect(url_for('main.dashboard'))
    found_mentors = []
    users = User.query.all()
    for user in users:
        if user.mentor is True and current_user.location.lower() == user.location.lower():
            found_mentors.append(user)

    return render_template('mentor.html', name=current_user.username, found_mentors=found_mentors)


@main.route('/courses')
@login_required
def courses():
    found_courses = []
    with open('coursera_courses.csv', 'r', errors='ignore') as read_obj:
        csv_reader = reader(read_obj)
        prefs = current_user.prefs.split(",")
        for row in csv_reader:
            for s_norm in row:
                s_lower = s_norm.lower()
                for pref in prefs:
                    if pref != "" and pref.lower() in s_lower and s_norm not in found_courses:
                        found_courses.append(s_norm)

    return render_template('courses.html', name=current_user.username, courses=found_courses)


@main.route('/scholarships')
@login_required
def scholarships():
    return render_template('scholarship.html', name=current_user.username)


@main.route('/preferences')
@login_required
def preferences():
    return render_template('preferences.html', name=current_user.username)


@main.route('/preferences', methods=['POST'])
def preferences_post():
    new_pref = request.form.get('add_pref')
    del_pref = request.form.get('del_pref')
    user_prefs = current_user.prefs

    # Both forms empty
    if new_pref == "" and del_pref == "":
        flash('Please enter a preference to add or delete!')
        return redirect(url_for('main.preferences'))

    # Delete prefs was not empty
    if new_pref == "" and del_pref != "":
        if del_pref not in user_prefs.split(","):
            flash('Please enter a VALID preference')
            return redirect(url_for('main.preferences'))
        new_pref_string = ""
        non_deleted_prefs = []
        for pref in user_prefs.split(","):
            if pref != del_pref:
                non_deleted_prefs.append(pref)
        current_user.prefs = ','.join(non_deleted_prefs)
        db.session.commit()
        return redirect(url_for('main.preferences'))

    if new_pref != "" and del_pref == "":
        if new_pref in user_prefs.split(","):
            flash('Please enter a NEW preference')
            return redirect(url_for('main.preferences'))
        new_user_prefs = user_prefs + "," + new_pref
        current_user.prefs = new_user_prefs
        db.session.commit()
        return redirect(url_for('main.preferences'))

    if new_pref == del_pref:
        flash('You cannot add and delete at the same time!')

    return redirect(url_for('main.preferences'))


@main.route('/duke_courses')
@login_required
def duke_courses():
    found_courses = find_personal_courses(current_user.prefs.split(","))
    header = found_courses.pop(0)
    return render_template('duke_courses.html', name=current_user.username, header=header, found_courses=found_courses)

