import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request
from datetime import datetime
from DataLayer import DataLayer
from Human import Student
from typing import Dict, Optional

app = Flask(__name__)

students_dict = {}
file = "Data/students.json"


@app.before_first_request
@app.route('/')
def create_data_layer_instance():
    data_layer = DataLayer()
    data_layer.load_all_students(file)
    return app.response_class(response=json.dumps(students_dict), status=200, mimetype="application/json")


@app.route('/students/<email>')
def get_students_by_email(email):
    pass


@app.route('/students')
def get_all_students():
    pass


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
    Student.add_new_student(data, students_dict)
    new_student = Student(data['student_id'], data['first_name'], data['last_name'], data['email'], data['password'],
                          data['existing_magic_skills'], data["desired_magic_skills"])
    students_dict[new_student.email] = new_student
    DataLayer.persist_students(new_student)


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
