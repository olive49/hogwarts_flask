import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from DataLayer import DataLayer
from Human import Student
from typing import Dict, Optional
from functools import wraps
from flask_cors import CORS
import atexit


app = Flask(__name__)
CORS(app)
app.secret_key = "Gryffindor"

data_layer = DataLayer()

#
# @atexit.register()
# def close_db_connection():
#     data_layer.shutdown()


@app.route('/')
def return_all_students():
    data_layer.get_all_students()
    return app.response_class(response=json.dumps(data_layer.students_dict),
                              status=200,
                              mimetype="application/json")

@app.route('/main')
def return_desired_skills_count():
    data_layer.get_desired_skills_count()
    return app.response_class(response=json.dumps(data_layer.desired_skills_dict), status=200, mimetype="application/json")

@app.route('/')
def return_existing_skills_count():
    data_layer.get_existing_skills_count()
    return app.response_class(response=json.dumps(data_layer.existing_skills_dict), status=200, mimetype="application/json")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('admin_login'))
        return wrap


@app.route('/students/<email>')
def get_students_by_email(email):
    for email in data_layer.students_dict:
        print(data_layer.students_dict[email])
    data_layer.get_student_by_email(email)
    return app.response_class(response=data_layer.students_dict[email],
                              status=200,
                              mimetype='application/json')


@app.route('/students')
def get_all_students():
    students = data_layer.get_all_students()
    return app.response_class(response=json.dumps(students),
                              status=200,
                              mimetype='application/json')


@app.route('/students/added_on/<added_date>')
def get_students_by_add_date(added_date):
    return app.response_class(response=data_layer.get_students_by_add_date(added_date),
                              status=200,
                              mimetype='application/json')


@app.route('/students/desired_skills/<skill>')
def get_students_desired_skills(skill):
    return app.response_class(response=data_layer.get_students_by_desired_skills(skill),
                              status=200,
                              mimetype='application/json')


@app.route('/students/existing_skills/<skill>')
def get_students_existing_skills(skill):
    return app.response_class(response=data_layer.get_students_by_existing_skills(skill),
                              status=200,
                              mimetype='application/json')


@app.route('/students/add', methods=["POST"])
def add_student():
    if request.method == "POST":
        data = request.json
        Student.add_new_student(data)
        new_student = Student(data['first_name'], data['last_name'], data['email'],
                              data['existing_magic_skills'], data["desired_magic_skills"])
        dict_student = new_student.__dict__
        result = data_layer.add_student(dict_student)
        response = app.response_class(response=json.dumps(result),
                                      status=200, mimetype="application/json")
        return response


@app.route('/students/edit/<email>', methods=["PUT"])
def edit_student(email):
    if request.method == "PUT":
        data = request.json
        Student.edit_student(data)
        result = data_layer.edit_student(data, email)
        response = app.response_class(response=json.dumps(result),
                                      status=200, mimetype="application/json")
        return response


@app.route('/admin/signup', methods=["POST"])
def admin_signup():
    error = None
    if request.method == "POST":
        data = request.json
        return data


@app.route('/admin/login', methods=["POST"])
def admin_login():
    error = None
    if request.method == 'POST':
        msg = {'msg': 'bad password or username'}
        data = request.json
        session['logged_in'] = True
        flash("Welcome, Admin")
        result = data_layer.is_admin(data)
        if result is True:
            msg = {'msg': 'welcome admin'}
        return app.response_class(response=json.dumps(msg),
                                  status=200,
                                  mimetype="application/json")


@app.route('/student/login', methods=["PUT", "GET"])
def student_login():
    error = None
    if request.method == 'PUT':
        data = request.json
        if data['username'] is None or data['password'] is None:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("Welcome, Student")
            return redirect(url_for('edit_student'))
    # return render_template('edit_student.html', error=error)


@app.route('/students/edit/desired_skills', methods=["PUT"])
def edit_student_desired_skills():
    data = request.json
    email = data["email"]
    desired_skills = data["desired_magic_skills"]
    student = data_layer.students_dict[email]
    Student.edit_student(student, data_layer.students_dict)
    Student.add_desired_skills(student, desired_skills)
    data_layer.persist_students()
    app.response_class(response=({"Student updated"}),
                       status=200, mimetype="application/json")
    return data_layer.load_all_students()


@app.route('/students/edit/existing_skills', methods=["PUT"])
def edit_student_existing_skills():
    data = request.json
    email = data["email"]
    new_existing_skill = data["existing_magic_skills"]
    student = data_layer.students_dict[email]
    Student.edit_student(student, data_layer.students_dict)
    Student.add_existing_skill(student, new_existing_skill)
    data_layer.persist_students()
    app.response_class(response=({"Student updated"}),
                       status=200, mimetype="application/json")
    return data_layer.load_all_students()


@app.route('/students/delete/<email>', methods=["DELETE"])
def remove_student(email):
    data_layer.remove_student(email)
    return "Student removed"

@app.route('/students/delete/all', methods=["DELETE"])
def remove_all_students():
    data_layer.remove_all_students()
    return "All students removed"


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
