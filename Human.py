import json
import datetime as datetime
from Validators import Validators
from datetime import datetime
import time
from typing import Dict, Optional
from Skill import Skill
from MongoDaterLayer import MongoDataLayer
import os
import hashlib


class Human:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


    def get_email(self):
        return self.email


class Student(Human):

    mongoDB = MongoDataLayer()

    last_update = str(datetime.now())

    def __init__(self, first_name, last_name, email,
                 existing_magic_skills=[], desired_magic_skills=[]):
        super().__init__(first_name, last_name, email)

        existing_magic_skills_as_object = []
        for existing_skill_string in existing_magic_skills:
            existing_magic_skills_as_object.append(Skill(existing_skill_string))
            print(Skill(existing_skill_string))

        desired_magic_skills_as_object = []
        for desired_skill_string in desired_magic_skills:
            desired_magic_skills_as_object.append(Skill(desired_skill_string))
            print(Skill(desired_skill_string))

        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills
        self.creation_time = str(datetime.now().date())
        self.last_update = str(datetime.now())

    @staticmethod
    def add_existing_skill(student, skill):
        student["existing_magic_skills"].append(skill)
        last_update = str(datetime.now())
        student["last_update"] = last_update

        return student

    @staticmethod
    def add_desired_skills(student, skill):
        student["desired_magic_skills"].append(skill)
        last_update = str(datetime.now())
        student["last_update"] = last_update

        return student

    @staticmethod
    def from_json(student_json):
        student_dict = json.loads(student_json)
        new_student = Student(student_dict["first_name"], student_dict["last_name"],
                              student_dict["email"], student_dict["existing_magic_skills"],
                              student_dict["desired_magic_skills"])

        return new_student

    @staticmethod
    def add_new_student(student):
        students_dict = Student.mongoDB.get_all_students()
        Validators.all_required_fields(student)
        Validators.validate_name(student['first_name'], student['last_name'])
        Validators.validate_email(student['email'])
        # Validators.validate_id(student['student_id'])
        Validators.unique_email(student['email'], students_dict)
        return student

    @staticmethod
    def edit_student(student):
        students_dict = Student.mongoDB.get_all_students()
        Validators.all_required_fields(student)
        Validators.validate_name(student["first_name"], student["last_name"])
        Validators.validate_email(student["email"])
        # Validators.validate_student_exists(student, students_dict)
        student["last_update"] = str(datetime.now())

    def student_login(self):
        Validators.all_required_fields(self)
        Validators.validate_name(self.first_name, self.last_name)
        Validators.validate_email(self.email)
        Validators.validate_password(self.password)
        Validators.validate_id(self.id)

    def get_student_by_email(self):
        Validators.email_provided(self.email)
        Validators.validate_email(self.email)


class Admin(Human):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email)
        self.__password = password

    salt = os.urandom(32)
    password = 'password123'

    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )

    storage = salt + key
        # send a request so it knows this user is the admin
