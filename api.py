import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request
from datetime import datetime
from DataLayer import DataLayer
from Human import Student
from typing import Dict, Optional

app = Flask(__name__)
data_layer = DataLayer()


@app.before_first_request
@app.route('/')
def create_data_layer_instance():
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


@app.route('/students/add', methods=["PUT"])
def add_student():
    data = request.json
    Student.add_new_student(data, data_layer.students_dict)
    new_student = Student(data['student_id'], data['first_name'], data['last_name'], data['email'], data['password'],
                          data['existing_magic_skills'], data["desired_magic_skills"])
    data_layer.set_student_by_email(new_student, new_student.email)
    data_layer.students_dict[new_student.email] = new_student
    print(data_layer.students_dict)
    data_layer.persist_students()
    print(new_student)
    return "Student added"


@app.route('/students/login', methods=["PUT", "GET"])
def student_login():
    pass


@app.route('/students/edit/<email>', methods=["PUT"])
def edit_student(email):
    for email in data_layer.students_dict:
        print(data_layer.students_dict.get(email))
    # student.edit_student(email)


@app.route('/students/delete/<email>', methods=["POST"])
def remove_student(email):
    data_layer.remove_student(email)
    data_layer.persist_students()
    return "Student removed"


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
