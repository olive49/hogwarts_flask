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
    DataLayer.get_student_by_email(email, DataLayer)
    return data_layer.students_dict[email]


@app.route('/students')
def get_all_students():
    for key, value in data_layer.students_dict:
        print(key, value)
    return app.response_class(response=json.dumps(data_layer.students_dict),
                              status=200,
                              mimetype='application/json')


@app.route('/students/added_on/<int:added_date>')
def get_students_by_add_date():
    pass


@app.route('/students/desired')
def get_students_desired_skills():
    return


@app.route('/students/skills')
def get_skills():
    return


@app.route('/students/add', methods=["PUT"])
def add_student():
    data = request.json
    Student.add_new_student(data, data_layer.students_dict)
    new_student = Student(data['student_id'], data['first_name'], data['last_name'], data['email'], data['password'],
                          data['existing_magic_skills'], data["desired_magic_skills"])
    data_layer.students_dict[new_student.email] = new_student
    # print(data_layer.students_dict)
    data_layer.persist_students(new_student)
    return "Student added"


@app.route('/students/login', methods=["PUT"])
def student_login():
    pass


@app.route('/students/edit/<id>', methods=["PUT"])
def edit_student(id):
    pass


@app.route('/students/delete/<id>', methods=["PUT"])
def delete_student(id):
    pass


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)

