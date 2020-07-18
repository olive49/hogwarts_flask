import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from DataLayer import DataLayer
from Human import Student
from typing import Dict, Optional
from functools import wraps

app = Flask(__name__)
data_layer = DataLayer()
app.secret_key = "Gryffindor"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('admin_login'))
        return wrap


@app.before_first_request
@app.route('/')
def return_all_students():
    data_layer.load_all_students()
    return app.response_class(response=json.dumps(data_layer.students_dict), status=200, mimetype="application/json")


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
    for key, value in data_layer.students_dict:
        print(key, value)
    return app.response_class(response=json.dumps(data_layer.students_dict),
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


@app.route('/students/add', methods=["PUT", "GET"])
# @login_required
def add_student():
    data = request.json
    Student.add_new_student(data, data_layer.students_dict)
    new_student = Student(data['student_id'], data['first_name'], data['last_name'], data['email'],
                          data['password'],
                          data['existing_magic_skills'], data["desired_magic_skills"])
    data_layer.set_student_by_email(new_student, new_student.email)
    data_layer.students_dict[new_student.email] = new_student
    data_layer.persist_students()
    response = app.response_class(response=({"New student added"}),
                                  status=200, mimetype="application/json")
    return response


@app.route('/admin/login', methods=["PUT", "GET"])
def admin_login():
    error = None
    if request.method == 'PUT':
        data = request.json
        if data['username'] != 'admin' and data['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("Welcome, Admin")
            return redirect(url_for('add_student'))
    # return render_template('add_student.html', error=error)


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


@app.route('/students/edit/<email>', methods=["PUT", "GET"])
def edit_student(email):
    student = data_layer.students_dict[email]
    # student_json = json.loads(student)
    if request.method == 'PUT':
        data = request.json
        Student.add_desired_skills(student, data)
        data_layer.persist_students()
        app.response_class(response=({"Student updated"}),
                           status=200, mimetype="application/json")
        return data_layer.load_all_students()

        # return json.dumps(data_layer.students_dict[email])
    # student.edit_student(email)


@app.route('/students/delete/<email>', methods=["POST"])
def remove_student(email):
    data_layer.remove_student(email)
    data_layer.persist_students()
    return "Student removed"


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
