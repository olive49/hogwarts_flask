import json

import datetime as datetime

# from DataLayer import DataLayer
from Validators import Validators
from datetime import datetime
from typing import Dict, Optional


class Human:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_email(self):
        return self.email


class Student(Human):
    def __init__(self, student_id, first_name, last_name, email, password,
                 existing_magic_skills=[], desired_magic_skills=[]):
        super().__init__(first_name, last_name, email, password)
        self.id = student_id
        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills
        self.creation_time = str(datetime.now().isoformat())
        self.last_update = str(datetime.now().isoformat())

    def __str__(self):
        local_student_dict = {self.email: {"first_name": self.first_name,
                                           "last_name": self.last_name,
                                           "email": self.email,
                                           "password": self.password,
                                           "existing_magic_skills": self.existing_magic_skills,
                                           "desired_magic_skills": self.desired_magic_skills
                                           }}
        string = "{}".format(local_student_dict)
        json.dumps(string, default=lambda o: o.__dict__)
        return string
        # existing_magic_skills = ''
        # for skills in self.existing_magic_skills:
        #     existing_magic_skills += skills.__str__()
        # if len(existing_magic_skills) == 0:
        #     existing_magic_skills = 'None'
        #
        # desired_magic_skills = ''
        # for skills in self.desired_magic_skills:
        #     desired_magic_skills += skills.__str__()
        # if len(desired_magic_skills) == 0:
        #     desired_magic_skills = 'None'

    def add_existing_skill(self, skill):
        self.existing_magic_skills.append(skill)
        print(self.existing_magic_skills)

    def add_desired_skills(self, skill):
        self.desired_magic_skills.append(skill)
        print(self.desired_magic_skills)

    @staticmethod
    def from_json(student_json):
        student_dict = json.loads(student_json)
        new_student = Student(student_dict["student_id"], student_dict["first_name"], student_dict["last_name"],
                              student_dict["email"], student_dict["password"], student_dict["existing_magic_skills"],
                              student_dict["desired_magic_skills"])

        return new_student

    @staticmethod
    def add_new_student(student, students_dict):
        Validators.all_required_fields(student)
        Validators.validate_name(student['first_name'], student['last_name'])
        Validators.validate_email(student['email'])
        Validators.validate_password(student['password'])
        Validators.validate_id(student['student_id'])
        Validators.unique_email(student['email'], students_dict)
        return student, students_dict

    def edit_student(self, students_dict):
        Validators.all_required_fields(self)
        Validators.validate_name(self.first_name, self.last_name)
        Validators.validate_email(self.email)
        Validators.validate_password(self.password)
        Validators.validate_student_exists(self, students_dict)
        Validators.validate_id(self.id)

    def student_login(self):
        Validators.all_required_fields(self)
        Validators.validate_name(self.first_name, self.last_name)
        Validators.validate_email(self.email)
        Validators.validate_password(self.password)
        Validators.validate_id(self.id)

    def get_student_by_email(self):
        Validators.email_provided(self.email)
        Validators.validate_email(self.email)

    def get_added_students_per_date(self):
        pass


class Admin(Human):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
