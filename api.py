import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request
from datetime import datetime
from DataLayer import DataLayer

app = Flask(__name__)

students_dict = {}
file = "Data/students.json"

@app.before_first_request
def create_data_layer_instance():
    datalayer = DataLayer(students_dict)
    datalayer.load_all_students(file)


@app.route('/students/<email>')
def get_students_by_email(email):
    pass


@app.route('/students')
def get_all_students():
    pass


# @app.route('/students/', params=datetime.now.__str__())
# def get_students_by_add_date():
#     pass


@app.route('/students/desired')
def get_students_desired_skills():
    return


@app.route('/students/skills')
def get_skills():
    return


@app.route('/students/add', methods=["POST"])
def add_student():
    pass


@app.route('/students/login', methods=["POST"])
def student_login():
    pass


@app.route('/students/edit/<id>', methods=["POST"])
def edit_student(id):
    pass


@app.route('/students/delete/<id>', methods=["POST"])
def delete_student(id):
    pass


if __name__ == "__main__":
    app.run()
