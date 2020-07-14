import json
import os.path, time
from flask import Flask, send_from_directory, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.route('/students/<email>')
def get_students_by_email(email):
    pass


@app.route('/students')
def get_all_students():
    pass


@app.route('/students/', params=datetime.now.__str__())
def get_students_by_add_date(date):
    pass


@app.route('/students/desired')
def get_students_desired_skills():
    return


@app.route('/students/skills')
def get_skills():
    return


@app.route('/students/add', methods=["POST"])
def add_student():
    pass


@app.route('students/login', method=["POST"])
def student_login():
    pass


@app.route('students/edit/<id>', method=["POST"])
def edit_student(id):
    pass


@app.route('students/delete/<id>', method=["POST"])
def delete_student(id):
    pass


if __name__ == "__main__":
    app.run()
