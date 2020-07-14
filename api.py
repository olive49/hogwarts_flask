import json
import os
from flask import Flask, send_from_directory, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.route('/students/<email>')
def get_students_by_email(email):
    print(email)
    return email


@app.route('/students')
def get_all_students():
    return


@app.route('/students/<date>')
def get_students_by_add_date(date):
    print(date)
    return date


@app.route('/students/desired')
def get_students_desired_skills():
    return


@app.route('/students/skills')
def get_skills():
    return


@app.route('/students/add', methods=["POST"])
def add_student():
    return "Student added"


@app.route('students/login', method=["POST"])
def student_login():
    return "Student logged in"


@app.route('students/edit/<id>', method=["POST"])
def edit_student(id):
    return "Student edited"


@app.route('students/delete/<id>', method=["POST"])
def delete_student(id):
    return "Student deleted"


if __name__ == "__main__":
    app.run()
